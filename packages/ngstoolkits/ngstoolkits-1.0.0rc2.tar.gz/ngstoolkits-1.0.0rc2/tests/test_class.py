"""
    Dummy conftest.py for ngstools.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

# import pytest
import sys
sys.path.append('src/ngstoolkits')
from ngs_class import cpra
import pytest

import sequence

mua_a = mutation_cpra()
sequence.get_oneletter_hgvsp("p.Ala1234Thr")

def test_single_mutation():
    mutation=ngs_class.cpra("chr19","1231","G","CT")
    assert mutation.type=="INS"
    mutation=ngs_class.cpra("chr19","1231","GTCA","CT")
    assert mutation.type=="DEL"
    mutation=ngs_class.cpra("chr19","1231","GA","CT")
    assert mutation.type=="SNV"
