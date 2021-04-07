# -*- coding: utf-8 -*-

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
                     'pyaerocom.web',
                     'pyaerocom.web.cli',
                     'pyaerocom.test',
                     'pyaerocom.io.test',
                     'pyaerocom.scripts'],
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
    description = ('pyaerocom model evaluation software'),
    long_description = readme,
    long_description_content_type='text/x-rst',
    entry_points = {'console_scripts' : [
            'pya=pyaerocom.scripts.cli:main',
            'pyaeroeval=pyaerocom.web.cli.main_aerocom_evaluation:main'
            ]},
    zip_safe = False
)
