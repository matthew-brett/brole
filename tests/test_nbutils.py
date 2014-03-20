""" Test notebook utilities """

from os.path import join as pjoin, dirname

from IPython.nbformat import current as nbf

from brole.nbutils import clear_output, cellgen

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
    # Load a notebook with some output
    eg_nb_fname = pjoin(TINYPAGES, 'mini_full.ipynb')
    with open(eg_nb_fname, 'rt') as fobj:
        json = fobj.read()
    nb_with_output = nbf.reads_json(json)
    assert_true(_has_output(nb_with_output))
    # Clear output with default copy=True
    nb_no_output = clear_output(nb_with_output)
    # Return value has no output
    assert_false(_has_output(nb_no_output))
    # Original unchanged
    assert_true(_has_output(nb_with_output))
    # Original changed if copy=False
    nb_no_output = clear_output(nb_with_output, copy=False)
    assert_false(_has_output(nb_no_output))
    assert_false(_has_output(nb_with_output))
