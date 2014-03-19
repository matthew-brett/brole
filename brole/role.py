""" Sphinx role for static notebook """
from __future__ import print_function

import os
from os.path import (join as pjoin, relpath, splitext,
                     abspath, dirname, exists)

from datetime import datetime

from docutils import nodes, utils

from sphinx.util.nodes import split_explicit_title

from IPython.nbformat import current as nbf

from .nbutils import evaluate_nb_file, clear_output, nb_to_html, nb_to_py

DATE_FMT = "%a, %d %h %Y %H:%M:%S UTC"
HOME = dict(icon = 'chevron-left', text = 'Home', url = '../')

def _rel_url(link_path, page_path):
    page2link = relpath(link_path, page_path)
    if os.sep == '\\':
        page2link = page2link.replace('\\', '/')
    return page2link


def brole(typ, rawtext, text, lineno, inliner, options={}, content=[],
         evaluate=False):
    """ Role for building and linking to notebook html pages

    Parameters
    ----------
    name : str
        The role name used in the document.
    rawtext : str
        The entire markup snippet, with role.
    text : str
        The text marked with the role.
    lineno : int
        The line number where `rawtext` appears in the input.
    inliner : object
        The inliner instance that called us.
    options : dict
        Directive options for customization.
    content : content
        The directive content for customization.

    Returns
    -------
    nodes : list
        list of nodes to insert into the document. Can be empty.
    messages : list
        list of system messages. Can be empty
    """
    doc = inliner.document
    env = doc.settings.env
    app = env.app
    j2_env = app.builder.templates.environment
    text = utils.unescape(text)
    # Get title and link
    has_explicit, title, nb_fname = split_explicit_title(text)
    # Source notebook path
    nb_rel_path, nb_abs_path = env.relfn2path(nb_fname)
    # Corresponding output path
    nb_out_path = abspath(pjoin(app.outdir, nb_rel_path))
    dest_dir = dirname(nb_out_path)
    if not exists(dest_dir):
        os.makedirs(dest_dir)
    # Evaluate and copy to output directory
    if evaluate:
        nb = evaluate_nb_file(nb_abs_path)
    else:
        with open(nb_abs_path, 'rt') as fobj:
            nb = nbf.read(fobj, 'json')
    out_root, ext = splitext(nb_out_path)
    html_fname = out_root + '.html'
    # Where is the notebook compared to source?
    src_rel_path, _ = env.relfn2path('.')
    page_out_path = abspath(pjoin(app.outdir, src_rel_path))
    def _get_url(fname):
        return _rel_url(fname, page_out_path)
    # Inject pathto into jinja
    rel_to_root = _rel_url(app.outdir, page_out_path)
    def _pathto(otheruri, _):
        return '/'.join([rel_to_root, otheruri])
    # import IPython; IPython.embed()
    if not exists(nb_out_path): # Already done
        with open(nb_out_path, 'wt') as fobj:
            nbf.write(nb, fobj, 'json')
        # Create stripped version
        stripped_fname = out_root + '_stripped.ipynb'
        with open(stripped_fname, 'wt') as fobj:
            nbf.write(clear_output(nb), fobj, 'json')
        # Make script
        py_fname = out_root + '.py'
        with open(py_fname, 'wt') as fobj:
            fobj.write(nb_to_py(nb)[0])
        # Make html
        html, resources = nb_to_html(nb)
        downloads = {'Notebook': _get_url(nb_out_path),
                     'Notebook (stripped)': _get_url(stripped_fname),
                     'Notebook as Python script': _get_url(py_fname)}
        resources.update(nbhtml = html,
                         pathto = _pathto,
                         home = HOME,
                         date=datetime.utcnow().strftime(DATE_FMT),
                         downloads=downloads)
        template = j2_env.get_template('css_js_notebook.html')
        wrapped_html = template.render(resources)
        with open(html_fname, 'wt') as fobj:
            fobj.write(wrapped_html)
    # Return link node
    # url = config.cheeseshop_url + '/' + nb_fname
    ref = nodes.reference(rawtext, title, refuri=_get_url(html_fname))
    return [ref], []


def ebrole(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """" Role to force evaluation of notebook when building """
    return brole(typ, rawtext, text, lineno, inliner, options={}, content=[],
                 evaluate=True)


def setup(app):
    app.add_role('brole', brole)
    app.add_role('ebrole', ebrole)
    app.add_config_value('cheeseshop_url',
                         'http://pypi.python.org/pypi', 'html')
