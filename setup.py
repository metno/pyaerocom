from setuptools import setup

with open('README.rst') as file:
    readme = file.read()

with open('VERSION.md') as f:
    version = f.readline()
    print(version)
    f.close()

setup(
    name        =   'pyaerocom',
    version     =   version,
    author      =   'MET Norway',
    url         =   'https://github.com/metno/pyaerocom.git',
    license     =   'GPLv3',
    package_dir =   {'pyaerocom'      :   'pyaerocom'},
    packages    =   ['pyaerocom',
                     'pyaerocom.io',
                     'pyaerocom.plot',
                     'pyaerocom.tools',
                     'pyaerocom.aeroval',
                     'pyaerocom.scripts'],
    package_data=   {'pyaerocom'    :   ['data/*']},

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering :: Atmospheric Science',

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.,
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    python_requires = '>=3.7,<4',
    install_requires = [
        'scitools-iris>=3.0.1,<3.1.0',
        'scitools-pyke>=1.1.1',
        'xarray>=0.16.0',
        'cartopy>=0.16.0',
        'matplotlib>=3.0.1',
        'scipy>=1.1.0',
        'pandas>=0.23.0',
        'seaborn>=0.8.0',
        'geonum',
        'LatLon23', # required by geonum
        'SRTM.py', # required by geonum
        'numpy',
        'simplejson',
        'requests',
        'reverse-geocode',
        'tqdm',
        'openpyxl',
        'geojsoncontour'
    ],
    extras_require = {
        'docs':['nbsphinx'],
        'test':['pytest>=6.0','pytest-dependency','pytest-cov'],
    },
    dependency_links    =   [],
    description = ('pyaerocom model evaluation software'),
    long_description = readme,
    long_description_content_type='text/x-rst',
    entry_points = {'console_scripts' : [
            'pya=pyaerocom.scripts.cli:main'
            ]},
    zip_safe = False
)
