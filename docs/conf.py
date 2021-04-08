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
import os, sys, subprocess

# -- clone pyaerocom-tutorials repo --------------------------------------
TUTREPO = 'pyaerocom-tutorials'
TUTURL = f'https://github.com/metno/{TUTREPO}.git'

def init_tutorials():
    if not 'conf.py' in os.listdir():
        raise FileNotFoundError('Wrong directory...')

    if not TUTREPO in os.listdir():
        command = f'git clone {TUTURL}'
        print(command)
        subprocess.call(command, shell=True)
    if not TUTREPO in os.listdir():
        raise FileNotFoundError('Failed to clone pyaerocom-tutorials repo into '
                                'pyaerocom/docs')

print('Initiating pyaerocom-tutorials repo under pyaerocom/docs')
init_tutorials()

# -- Add paths ---------------------------------------
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))



# -- Project information -----------------------------------------------------

project = 'pyaerocom'
copyright = '2018, MET Norway'
author = 'pyaerocom developers'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'nbsphinx'
]

intersphinx_mapping = {

    'python'    : ('https://docs.python.org/3', None),
    #'iris'      : ('https://scitools.org.uk/iris/docs/latest/', None),
    'xarray'    : ('http://xarray.pydata.org/en/stable/', None),
    'pandas'    : ('https://pandas.pydata.org/docs/', None),
    'numpy'     : ('https://numpy.org/doc/stable/', None),
    'scipy'     : ('https://docs.scipy.org/doc/scipy/reference/', None),
    }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
