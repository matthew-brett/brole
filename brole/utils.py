""" Utilities for brole package """

from os.path import join as pjoin, split as psplit, abspath, dirname

_HERE = dirname(__file__)

def get_static():
    """ Get static paths """
    return abspath(pjoin(_HERE, 'static'))


def get_templates():
    """ Get template paths """
    return abspath(pjoin(_HERE, 'templates'))
