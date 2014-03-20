################
Refactoring plan
################

It would be nice to allow building of notebook pages with differing back (home)
links depending on some configuration.

This could be done with something like::

    .. role:: nb-stack1(brole)
        :docname: stack1/index

Then::

    Here is a :nb-stack:`notebook in stack 1 <a_notebook.ipynb>`.

See `Custom interpreted text roles <http://docutils.sourceforge.net/docs/ref/rst/directives.html#custom-interpreted-text-roles>`_ in the docutils documentation.

The effect of the ``docname`` option would be to set any built pages to have
the home link point back to this document (``stack1/index.rst`` in source,
``stack1/index.html`` in build html).

This and the ``evaluate`` option (``brole`` vs ``ebrole``) will mean that it's
possible to have different output html from different versions of the notebook
role. This is a problem, because we could have different roles pointing the the
same notebook as in::

    Here's one with the default `home` - :brole:`a_notebook.ipynb`.

    Here's another with non-default - :nb-stack1:`a_notebook.ipynb`.

Or, (same idea)::

    Here's one with that gets evaluated - :ebrole:`a_notebook.ipynb`.

    Here's another that doesn't :brole:`a_notebook.ipynb`.

In this case we could just choose the first or second, but if the links are in
different documents, the 'first' and 'second' are somewhat arbitrary, depending
on sphinx's build order.

This makes it seem like it would be a good idea to disallow these invocations
above, and force something like::

    Here's one with that gets evaluated - :ebrole:`a_notebook.ipynb`.

    Here's another that just links back to the built notebook
    :nblink:`a_notebook.ipynb`.

We raise an error for two ``brole``-type roles trying to build the same
notebook in different ways (different options). Instead we suggest a ``nblink``
to the document for one of the competing broles.  We should also raise an error
if the ``nblink`` points to a notebook that doesn't exist.

To error for different broles on the same notebook, we can do this within the
role code itself, by caching somewhere a record of notebook files and used
options, and comparing to the cache when we see a new brole.  We'd have to
clear the cache somehow - see `Sphinx API docs <http://sphinx-doc.org/extdev/appapi.html>`_ expecially ``connect`` and the list of core events for one way of getting that done.

The bad links from ``nb-link`` is harder - we have to first go through all the
brole links, then the nb-links, so see if there are any that don't have a
corresponding brole links.

This might be best done by putting some temporary nodes into the doctree,
perhaps some corresponding data into the Sphinx ``env``, then, after parsing,
go back and analyze.  See `bibref <https://github.com/matthew-brett/bibstuff/blob/master/bibstuff/sphinxext/bibref.py>`_ for an example.

Doing this also means we might be able to check whether the html we are
building for the notebook will overwrite or be overwritten by html from the
rest of the doc build.
