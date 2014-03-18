""" Render ipython notebook html using template """
from __future__ import print_function

import sys
PY3 = sys.version_info[0] >= 3

from os.path import join as pjoin, split as psplit, abspath, dirname
import locale

from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from IPython.nbformat.current import reads_json
from jinja2 import Environment, FileSystemLoader

# Jinja2 config
here = dirname(__file__)
template_path = pjoin(here, 'templates')
j2_env = Environment(loader=FileSystemLoader(template_path))
j2_env.globals.update(
                     )

def render_notebook(exporter, json_notebook):
    nb = reads_json(json_notebook)
    return exporter.from_notebook_node(nb)


def export_notebook(nbjson, template, **kwargs):
    # NBConvert config
    config = Config()
    config.HTMLExporter.template_file = 'basic'
    config.NbconvertApp.fileext = 'html'
    config.CSSHTMLHeaderTransformer.enabled = False

    exporter = HTMLExporter(config=config)

    nbhtml, resources = render_notebook(exporter, nbjson)
    resources.update(nbhtml=nbhtml,
                     **kwargs
                    )
    return template.render(resources)


def main():
    fname = sys.argv[1]
    with open(fname, 'rt') as fobj:
        nbjson = fobj.read()

    home = dict(icon = 'chevron-left',
                text = 'Home',
                url = '../')

    from datetime import datetime
    date_fmt = "%a, %d %h %Y %H:%M:%S UTC"

    downloads = {"Notebook File" : fname, "Notebook File (Again)" : fname}

    template = j2_env.get_template('css_js_notebook.html')
    html = export_notebook(nbjson,
                           template,
                           home = home,
                           date=datetime.utcnow().strftime(date_fmt),
                           downloads=downloads)
    if PY3: # sys.stdout is unicode string stream
        print(html)
        return
    # Python 2 - need to guess encoding if not known
    std_enc = sys.stdout.encoding
    if std_enc is None: # often is for pipes
        std_enc = locale.getdefaultlocale()[1]
    print(html.encode(std_enc))
