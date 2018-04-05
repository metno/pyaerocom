# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as file:
    readme = file.read()

with open('VERSION.md') as f:
    version = f.readline()
    f.close()


setup(
    name        =   'pyaerocom',
    version     =   version,
    author      =   'Jonas Gliss',
    author_email=   'jonas.gliss@met.no',
    url         =   'https://github.com/jgliss/pyaerocom.git',
    license     =   'GPLv3',
    package_dir =   {'pyaerocom'      :   'pyaerocom'},
    packages    =   ['pyaerocom',
                     'pyaerocom.read',
                     'pyaerocom.plot'], #find_packages(exclude=['contrib', 'docs', 'tests*']),
    #include_package_data = True,            
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

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.,
        'Programming Language :: Python :: 3.6'
    ],

    install_requires    =   [],
    dependency_links    =   [],
    description = ('Python software for Aerocom related analyses and '
                   ' comparisons of global aerosol model data (e.g. ECMWF) and '
                   'observations (e.g. Aeronet, Satellite observations)'),
    long_description = readme,
)