# brole - a sphinx role for IPython notebooks

Install with usual ``python setup.py install``

After this you should be able to do:

    >>> import brole

See `tests/tinypages/conf.py` for how to configure your project to use
`brole`.

Basic usage:

    Here is a good :brole:`Notebook I wrote <fancy_notebook.ipynb>`

This will cause the named notebook to get built into html and written into the
html build tree.

You can evaluate the notebook while you are building with `ebrole`:

    Here is a somewhat tested and rebuilt :ebrole:`Notebook I wrote
    <fancy_notebook.ipynb>`
