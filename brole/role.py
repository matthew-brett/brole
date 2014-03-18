""" Sphinx role for static notebook """

import re

from docutils import nodes, utils

from sphinx.util.nodes import split_explicit_title

def brole(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for building and linking to notebook html pages """
    env = inliner.document.settings.env
    text = utils.unescape(text)
    has_explicit, title, target = split_explicit_title(text)
    m = re.match(r'(.*)\s+\((.*?)\)', target)
    if m:
        dist, version = m.groups()
        url = env.config.cheeseshop_url + '/' + dist + '/' + version
        if not has_explicit:
            title = '%s %s' % (dist, version)
    else:
        url = env.config.cheeseshop_url + '/' + target
    ref = nodes.reference(rawtext, title, refuri=url)
    return [ref], []


def setup(app):
    app.add_role('brole', brole)
    app.add_config_value('cheeseshop_url',
                         'http://pypi.python.org/pypi', 'html')
