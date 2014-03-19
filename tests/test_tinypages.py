""" Tests for tinypages build using notebook page role """

import shutil

from os.path import (join as pjoin, split as psplit, abspath, dirname,
                     exists, isdir)

from subprocess import Popen, PIPE, check_call

from nose.tools import (assert_true, assert_false, assert_raises,
                        assert_equal, assert_not_equal)

HERE = dirname(__file__)
TINYPAGES = pjoin(HERE, 'tinypages')
TINYBUILD = pjoin(TINYPAGES, '_build')
TINYHTML = pjoin(TINYBUILD, 'html')


def setup():
    shutil.rmtree(pjoin(TINYPAGES, '_build'))
    doctrees = pjoin(TINYBUILD, 'doctrees')
    doctrees = pjoin(TINYBUILD, 'doctrees')
    check_call(['sphinx-build', '-b', 'html', '-d', doctrees,
                TINYPAGES, TINYHTML])


def test_smoke():
    assert_true(isdir(TINYHTML))
