import pysam
from collections import namedtuple
from functools import lru_cache

class cpra():
    """
    descriptrion a mutation in cpra( eg: chr1, 100, A, T)
    and get some useful information with Bam or reference genome:
    """

    reference=None
    bam=None

    @classmethod
    def loadReference(cls,reference):
        """
        load reference genome
        param reference: eg: d:\Git_Repo\package_ngstools\data\hg19.fa
        """
        if cls.reference is None:
            cls.reference = pysam.FastaFile(reference)
        else:
            cls.reference = pysam.FastaFile(reference)
            print("reference has been loaded & reloaded")

    @classmethod
    def loadBam(cls,Bam):
        """
        load bam file
        param Bam: eg: d:\Git_Repo\package_ngstools\data\test.bam
        """
        cls.bam = pysam.AlignmentFile(Bam)

    def __init__(self,CHROM:str,POS:int,REF:str,ALT:str):
        """
        Init a mutation object,
        param chrom: eg: chr1
        param pos: eg: 100
        param ref: eg: A
        param alt: eg: T
        """
        self.chrom = CHROM
        self.pos =  int(POS)
        self.ref = REF
        self.alt = ALT

    @property
    def muttype(self):
        if len(self.ref)>len(self.alt):
            return "DEL"
        elif len(self.ref)<len(self.alt):
            return "INS"
        else:
            return "SNV"

    @property
    def flank(self, length:int=10):
        '''获取变异的侧翼序列
        使用前需要通过loadReference(reference) 完成参考基因组的加载
        param length: 侧翼序列长度

        '''
        lbase = self.reference.fetch(self.chrom, self.pos-length,self.pos)
        rbase = self.reference.fetch(self.chrom, self.pos+len(self.ref), self.pos+len(self.ref)+length)
        return '..'.join((lbase, rbase))


    def guessbase(self):
        try:
            if self.reference.fetch(self.chrom, self.pos, self.pos+len(self.ref)) == self.ref:
                return 1
            elif self.reference.fetch(self.chrom, self.pos, self.pos+len(self.ref))== self.ref:
                return 0
            else:
                raise ValueError("ref sequence do not match with the genome file, check your data")
        except AttributeError as e:
            raise e.add_note("reference genome is not set, set it with cpra.loadReference(referencePath)")

    def get_suppot(self,bam_file, ref,coverflank=5):
        """
        get support for the mutation with special Bam File 
        param bam_file: bam file
        param ref: reference genome
        param coverflank: only the reads cover the ±coverflank(5) bases will be considered
        return: 
        support_reads_id,relation,cover_reads_id
        """
        self.support_reads = []
        self.support_readsID_list = []
        self.cover_readsID_list = []
        if self.muttype == "SNV":
            self.support_reads,self.support_readsID_list,self.cover_readsID_list = self.get_snv_support_reads(self, bam_file, ref,coverflank)
        elif self.muttype == "INS":
            self.support_reads,self.support_readsID_list,self.cover_readsID_list = self.get_ins_support_reads(self, bam_file, ref,coverflank)
        elif self.muttype == "DEL":
            self.support_reads,self.support_readsID_list,self.cover_readsID_list = self.get_del_support_reads(self, bam_file, ref,coverflank)
    @property
    @lru_cache
    def get_snv_support_reads(VcfMut, bam_file, ref,coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        Read = namedtuple('Read', ['read_name', 'pair', 'strand'])
        support_reads = []
        cover_reads = []
        start_reads = {}
        EndSite = VcfMut.pos + len(VcfMut.ref)
        for pileup_column in bam_file.pileup(region=str(VcfMut.chrom) + ':' + str(VcfMut.pos) + '-' + str(VcfMut.pos),mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip or (aln.flag > 1024) or (aln.mapping_quality < mapq) or \
                            aln.query_qualities[pileup_read.query_position] < baseq:
                        continue
                    start_reads[read] = [pileup_read.query_position, aln]
        for pileup_column in bam_file.pileup(region=str(VcfMut.chrom) + ':' + str(EndSite) + '-' + str(EndSite),
                                            stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    read_name = aln.query_name
                    pair = 'pe1' if aln.is_read1 else 'pe2'
                    strand = '-' if aln.is_reverse else '+'
                    read = Read(read_name, pair, strand)
                    if pileup_read.is_del or pileup_read.is_refskip:
                        continue
                    if read in start_reads:
                        start_query_position, start_aln = start_reads[read]
                        seq = start_aln.query_sequence[start_query_position:pileup_read.query_position]
                        cover_reads.append(aln)
                        if seq.upper() == VcfMut.alt.upper():
                            support_reads.append(aln)
        support_readIDs = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readIDs.append(aln.query_name)
        return [support_reads,support_readIDs,cover_readID_list]

    @lru_cache
    def get_ins_support_reads(VcfMut, bam_file, ref, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = VcfMut.pos + len(VcfMut.ref)
        CoverStart = VcfMut.pos-coverflank
        CoverEnd = EndSite + coverflank
        insLength=len(VcfMut.alt)-len(VcfMut.ref)
        for pileup_column in bam_file.pileup(region=str(VcfMut.chrom) + ':' + str(VcfMut.pos) + '-' + str(VcfMut.pos), mapq=mapq, baseq=baseq, stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name] = pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position and aln.cigarstring.find("I") > 0:
                            start = pileup_read.query_position-1
                            altstop = pileup_read.query_position - 1 +len(VcfMut.alt)
                            refstop = pileup_read.query_position-1 + len(VcfMut.ref)
                            if aln.query_sequence[start:altstop].upper() == VcfMut.alt.upper() and \
                                    aln.get_reference_sequence()[start:refstop].upper() == VcfMut.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position-insLength:pileup_read.query_position -insLength+ len(VcfMut.alt)].upper() == VcfMut.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position-insLength:pileup_read.query_position - insLength + len(VcfMut.ref)].upper() == VcfMut.ref.upper():
                                support_reads.append(aln)
                            elif aln.query_sequence[pileup_read.query_position:pileup_read.query_position + len(VcfMut.alt)].upper() == VcfMut.alt.upper() and \
                                aln.get_reference_sequence()[pileup_read.query_position:pileup_read.query_position + len(VcfMut.ref)].upper() == VcfMut.ref.upper():
                                support_reads.append(aln)
        support_readID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readID_list.append(aln.query_name)
        return [support_reads,support_readID_list,cover_readID_list]

    @lru_cache
    def get_del_support_reads(VcfMut, bam_file, ref, coverflank=5, mapq=20, baseq=20, overlaps=True, stepper="all", orphans=True):
        support_reads = []
        cover_reads = []
        bam = {}
        EndSite = VcfMut.pos + len(VcfMut.ref)
        CoverStart = VcfMut.pos-coverflank
        CoverEnd = EndSite + coverflank
        for pileup_column in bam_file.pileup(region=str(VcfMut.chrom) + ':' + str(VcfMut.pos) + '-' + str(EndSite), mapq=mapq , baseq = baseq,
                                            stepper=stepper, fastaFile=ref, max_depth=200000, **{"truncate": True}):
            if pileup_column.nsegments > 0:
                for pileup_read in pileup_column.pileups:
                    aln = pileup_read.alignment
                    bam[aln.query_name]=pileup_read
                    if (CoverStart in aln.positions) and (CoverEnd in aln.positions):
                        cover_reads.append(aln)
                        if pileup_read.query_position_or_next and aln.cigarstring.find("D") > 0:
                            start = pileup_read.query_position_or_next - 1
                            refstop = pileup_read.query_position_or_next + len(VcfMut.ref) - 1
                            altstop = pileup_read.query_position_or_next +len(VcfMut.alt) -1
                            if aln.get_reference_sequence()[start:refstop].upper() == VcfMut.ref.upper() and aln.query_sequence[start:altstop].upper() == VcfMut.alt.upper():
                                support_reads.append(aln)
                            elif aln.get_reference_sequence()[start+1:refstop+1].upper() == VcfMut.ref.upper() and aln.query_sequence[start+1:altstop+1].upper() == VcfMut.alt.upper():
                                support_reads.append(aln)
        support_readsID_list = []
        cover_readID_list = []
        for aln in cover_reads:
            cover_readID_list.append(aln.query_name)
        for aln in support_reads:
            support_readsID_list.append(aln.query_name)
        return [support_reads,support_readsID_list,cover_readID_list]

