""" Utilities for working with notebooks """

from IPython.config import Config
from IPython.nbconvert import python
from IPython.nbconvert.exporters import HTMLExporter, PythonExporter

from runipy.notebook_runner import NotebookRunner

# Tell notebook runner how to handle SVG
NotebookRunner.MIME_MAP['image/svg+xml'] = 'svg'

def cellgen(nb, type=None):
    """ Generator returning all cells from notebook `nb` of type `type`

    Parameters
    ----------
    nb : notebook object
    type : None or str
        If None, return all cells, otherwise return cells with this string as
        ``cell_type``

    Returns
    -------
    gen : generator
        Returns all cell for all worksheets where `type` matches
    """
    for ws in nb.worksheets:
        for cell in ws.cells:
            if type is None:
                yield cell
            elif cell.cell_type == type:
                yield cell


def clear_output(nb, copy=True):
    """ Clear code output from notebook `nb`, copying if asked

    If `copy` is False, modifies `nb` in-place.

    Parameters
    ----------
    nb : notebook object
    copy : {True, False}, optional
        If True, remove output from new copy of `nb`

    Returns
    -------
    nb : notebook object
        notebook with code output removed
    """
    if copy:
        nb = nb.copy()
    for cell in cellgen(nb, 'code'):
        if hasattr(cell, 'prompt_number'):
            del cell['prompt_number']
        cell.outputs = []
    return nb


def evaluate_nb_file(nb_in_path):
    """ Load and evaluate notebook at `nb_in_path`

    Parameters
    ----------
    nb_in_path : str
        path to notebook to evaluate

    Returns
    -------
    nb : notebook object
        Evaluated notebook object
    """
    nb_runner = NotebookRunner(nb_in=nb_in_path)
    nb_runner.run_notebook()
    return nb_runner.nb


def nb_to_html(nb, template_file = 'basic'):
    """ Convert notebook `nb` to html, using template `template_file`

    Parameters
    ----------
    nb : notebook object
    template_file : str, optional
        template to use for notebook conversion

    Returns
    -------
    html : str
        html output
    resources : ResourcesDict
        Resources
    """
    config = Config()
    config.HTMLExporter.template_file = template_file
    config.CSSHTMLHeaderTransformer.enabled = False
    exporter = HTMLExporter(config=config)
    return exporter.from_notebook_node(nb)


def nb_to_py(nb):
    """ Convert notebook `nb` to python file

    Parameters
    ----------
    nb : notebook object

    Returns
    -------
    pystr : str
        python code output
    resources : ResourcesDict
        Resources
    """
    exporter = PythonExporter()
    return exporter.from_notebook_node(nb)
