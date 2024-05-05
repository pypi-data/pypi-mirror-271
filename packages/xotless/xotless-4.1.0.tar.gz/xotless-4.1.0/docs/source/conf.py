# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------

project = "xotless"
author = "Merchise Autrement"

from datetime import datetime  # noqa

copyright = f"2012-{datetime.now().year} {author} [~º/~] and Contributors"
del datetime


# The full version, including alpha/beta/rc tags
try:
    from xotless._version import version

    release = version
except ImportError:
    from importlib import metadata
    from importlib.metadata import PackageNotFoundError

    try:
        dist = metadata.distribution("xotless")
        version = release = dist.version
    except PackageNotFoundError:
        version = "dev"
        release = "dev"


# -- General configuration ---------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
default_role = "code"
html_theme = "furo"
html_theme_options = {
    "light_css_variables": {
        "font-stack--monospace": '"Roboto Mono", "SFMono-Regular", Menlo, Consolas, Monaco, "Liberation Mono", "Lucida Console", monospace',
    },
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "py3": ("https://docs.python.org/3.10/", None),
    "hypothesis": ("https://hypothesis.readthedocs.io/en/latest/", None),
    "xotl.tools": ("https://merchise-autrement.gitlab.io/xotl.tools/", None),
}

# Maintain the cache forever.
intersphinx_cache_limit = 365

autosummary_generate = True

# Produce output for todo and todolist
todo_include_todos = True
