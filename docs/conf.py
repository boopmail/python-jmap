"""Sphinx configuration."""
project = "Python JMAP Bindings"
author = "Josh Finch"
copyright = "2023, Josh Finch"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
