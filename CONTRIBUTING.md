# DRAFT
# Contributing to pyaerocom

We're really happy that you want to contribute to pyaerocom!

The following are some guidelines for contributing to pyaerocom, a Python package containing reading, post analysis and visualisation tools for evaluating atmospheric models against observations in the form of station networks or satellite data. Pyaerocom was initially developed for the [AeroCom](http://aerocom.met.no) project. Pyaerocom is developed and maintained by climate and air quality researchers at the [Norwegian meteorological institute](http://www.met.no). As an open source project we welcome a varied user base and we are very open to contributions from our users.

## Some resources:
* [GitHub README](https://github.com/metno/pyaerocom/blob/main-dev/README.rst)
* [Website and documentation](https://pyaerocom.readthedocs.io/en/latest/index.html)
* [Evaluation portal](aeroval.met.no)

## Setting up a development environment
If you want to do changes to your pyaerocom code you should follow the [installation guide in the documentation](https://pyaerocom.readthedocs.io/en/latest/install.html) for "Installing from source into a conda environment" after setting up your environment in accordance with the requirements in the [pyaerocom_env.yml](https://github.com/metno/pyaerocom/blob/main-dev/pyaerocom_env.yml) file. Use the following installation command after cloning the repository

    pip install --no-deps -e .
    
to make the installation editable.

## Reporting bugs
If you find a bug, please report it using the [Issues](https://github.com/metno/pyaerocom/issues) tab in the pyerocom repository. The bug report should include as much information as possible to allow us to recreate the problem. 

## Questions about features or the API
If the documentation is unclear or you find and undocumented feature, questions can be submitted to the [Issues](https://github.com/metno/pyaerocom/issues) tab using the "question" label.

## Requesting enhancements
If you think of a feature that you want from pyaerocom you can add an issue describing it with the label "enhancement". Please describe the feature in some detail. You may also suggest how the API call for it would be. 

## Contributing code
You are welcome to contribute code to implement new features, fix bugs or contribute documentation. We work with pull requests so we can not allow direct edits to the code or documentation. If you want to contribute code changes you need to make the changes in a new branch (or a fork if you're an external contributor) and make a pull request to have your changes integrated into pyaerocom.

## Coding conventions
We are in the process of moving to the code style enforced by [black](https://github.com/psf/black). More details to come.

### Below here is text to help me write this file
    
    Welcome contributors to the project: Admit that you are eager for contributions and so happy they found themselves here.
    Table of Contents: If your CONTRIBUTING.md file is long, you might consider including a table of contents with links to different headings in your document. In github, each heading is given a URL by default, so you can link to that URL in the appropriate section of the Table of Contents for each heading. Do this in Markdown by wrapping the heading in [ ] and following with a parenthetical that includes the URL or header after # like [Reporting Bugs](#reporting-bugs).
    Short Links to Important Resources:
       docs: handbook / roadmap (you'll learn more about this in the roadmapping session)
       bugs: issue tracker / bug report tool
       comms: forum link, developer list, IRC/email
    Testing: how to test the project, where the tests are located in your directories.
    Environment details: how to set up your development environment. This might exist in the README.md depending on the project. If so, include a link.
    How to submit changes: Pull Request protocol etc. You might also include what response they'll get back from the team on submission, or any caveats about the speed of response.
    How to report a bug: Bugs are problems in code, in the functionality of an application or in its UI design; you can submit them through "bug trackers" and most projects invite you to do so, so that they may "debug" with more efficiency and the input of a contributor. Take a look at Atom's example for how to teach people to report bugs to your project.
    Templates: in this section of your file, you might also want to link to a bug report "template" like this one here which contributors can copy and add context to; this will keep your bugs tidy and relevant.
    First bugs for Contributors: Sometimes it is helpful to provide some guidelines for the types of bugs contributors should tackle (should they want to fix the bugs and not just submit them), see Atom's example section here.
    How to request an "enhancement" - enhancements are features that you might like to suggest to a project, but aren't necessarily bugs/problems with the existing code; there is a "label" for enhancments in Github's Issues (where you report bugs), so you can tag issues as "enhancement," and thereby allow contributors to prioritize issues/bugs reported to the project. See Atom's example section.
    Style Guide / Coding conventions - See Atom's example.
    Code of Conduct - You can make this part of CONTRIBUTING.md as Atom did to set the tone for contributions. You can also make this a separate Markdown file and link to it in CONTRIBUTING.md. You can also extend this section to link to your LICENSE.md or any details for project consumers on permissions and license details you have established for building on your work.
    Recognition model - provide a pre-emptive "thank you" for contributing and list any recognition contributors might receive for participating in your project.
    Who is involved? - Open Government's CONTRIBUTING.md has as a name/author, and it might be nice to have a more personal/friendly individual to attact to a project and reach out to with questions. You might list the core contributors and their preferred methods of contact here, or link to a humans.txt file in your root directory (same place as your CONTRIBUTING.md file), which lets people know who they are working. Here is an example of a humans.txt file.
    Where can I ask for help? - a nice extension to the previous section, with links to good comms channels for anyone with questions.
