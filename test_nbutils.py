""" Test notebook utilities """

from os.path import join as pjoin, split as psplit, abspath, dirname

from IPython.nbformat import current as nbf

from ..nbutils import clear_output, cellgen

from nose.tools import (assert_true, assert_false, assert_raises,
                        assert_equal, assert_not_equal)

HERE = dirname(__file__)
TINYPAGES = pjoin(HERE, 'tinypages')

def _has_output(nb):
    for cell in cellgen(nb, 'code'):
        if len(cell.outputs):
            return True
    return False


def test_clear_output():
    eg_nb_fname = pjoin(TINYPAGES, 'mini_full.ipynb')
    with open(eg_nb_fname, 'rt') as fobj:
        json = fobj.read()
    nb_with_output = nbf.reads_json(json)
    assert_true(_has_output(nb_with_output))
