# Contributing to pyaerocom

We're really happy that you want to contribute to pyaerocom!

The following are some guidelines for contributing to pyaerocom, a Python package containing reading, post analysis and visualisation tools for evaluating atmospheric models against observations in the form of station networks or satellite data. Pyaerocom was initially developed for the [AeroCom](http://aerocom.met.no) project. Pyaerocom is developed and maintained by climate and air quality researchers at the [Norwegian meteorological institute](http://www.met.no). As an open source project we welcome a varied user base and we are very open to contributions from our users.

## Some resources

* [GitHub README](https://github.com/metno/pyaerocom/blob/main-dev/README.rst)
* [Website and documentation](https://pyaerocom.readthedocs.io/en/latest/index.html)
* [Evaluation portal](aeroval.met.no)

## Setting up a development environment

If you want to do changes to your pyaerocom code you should follow the [installation guide in the documentation](https://pyaerocom.readthedocs.io/en/latest/install.html) for "Installing from source into a conda environment" after setting up your environment in accordance with the requirements in the [pyaerocom_env.yml](https://github.com/metno/pyaerocom/blob/main-dev/pyaerocom_env.yml) file. Use the following installation command after cloning the repository

``` bash
pip install --no-deps -e .
```

to make the installation editable.

## Reporting bugs

If you find a bug, please report it using the [Issues](https://github.com/metno/pyaerocom/issues) tab in the pyerocom repository. The bug report should include as much information as possible to allow us to recreate the problem.

## Questions about features or the API

If the documentation is unclear or you find and undocumented feature, questions can be submitted to the [Issues](https://github.com/metno/pyaerocom/issues) tab using the "question" label.

## Requesting enhancements

If you think of a feature that you want from pyaerocom you can add an issue describing it with the label "enhancement". Please describe the feature in some detail. You may also suggest how the API call for it would be.

## Contributing code

You are welcome to contribute code to implement new features, fix bugs or contribute documentation. We work with pull requests so we can not allow direct edits to the code or documentation. If you want to contribute code changes you need to make the changes in a new branch (or a fork if you're an external contributor) and make a pull request to have your changes integrated into pyaerocom.

### Tests

Any new functions/methods you add must be covered by tests. Tests are wirtten and run using pytest and are found under pyaerocom/tests. Missing test coverage will trigger a warning in the GitHub CI.

### Documentation

All new functions/methods/classes must have properly defined and written docstrings. Additional documentation may be provided (how to coming soon)

## Code conventions

We are in the process of moving to the code style enforced by [black](https://github.com/psf/black). More details to come.

## Pyaerocom team

* [Jan Griesfeller](https://github.com/jgriesfeller)
* [Alvaro Valdebenito](https://github.com/avaldebe)
* [Daniel Heinesen](https://github.com/dulte)
* [Augustin Mortier](https://github.com/AugustinMortier)
* [Jonas Gliß](https://github.com/jgliss) - former member
* [Hans Brenna](https://github.com/hansbrenna) - former member
