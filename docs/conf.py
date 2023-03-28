# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PTCQ'
copyright = '2023, Teddy van Jerry (Wuqiong Zhao)'
author = 'Teddy van Jerry (Wuqiong Zhao)'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_title = 'PTCQ'
html_theme_options = {
    "source_repository": "https://github.com/Teddy-van-Jerry/ptcq",
    "source_directory": "docs/",
}
html_static_path = ['_static']
