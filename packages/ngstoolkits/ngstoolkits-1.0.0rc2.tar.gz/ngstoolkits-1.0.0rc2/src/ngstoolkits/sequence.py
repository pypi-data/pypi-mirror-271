
def reverse_complement(base):
    base = base[::-1].upper()
    return base.replace('A', 't').\
                replace('C', 'g').\
                replace('T', 'a').\
                replace('G', 'c').upper()


acid_info = {
    'Ala': 'A', 'Arg': 'R', 'Asn': 'N', 'Asp': 'D',
    'Cys': 'C', 'Gln': 'Q', 'Glu': 'E', 'Gly': 'G',
    'His': 'H', 'Ile': 'I', 'Leu': 'L', 'Lys': 'K',
    'Met': 'M', 'Phe': 'F', 'Pro': 'P', 'Ser': 'S',
    'Thr': 'T', 'Trp': 'W', 'Tyr': 'Y', 'Val': 'V',
    'Ter': '*'
}
#@function_timer
def get_oneletter_hgvsp(hgvsp):
    '''获取单字母的hgvsp结果
    '''
    for acid in acid_info:
        if acid in hgvsp:
            hgvsp = hgvsp.replace(acid, acid_info[acid])
    return hgvsp
