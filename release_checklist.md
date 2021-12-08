# A list of ToDo's for official releases

**Preface:** For simplicity, in this example we will refer to the release number as ***version***, an example would be 1.0.0. Release candidate syntax will be indicated as ***version***.rcX where X denotes the number of the release candidate.

## Prepare release:

### Finalization of source code

- Fix and merge all open PR's associated with the release into the release branch.
- Make sure there are no open issues associated with the release.
- For the latter, check [milestones](https://github.com/metno/pyaerocom/milestones). If there are open issues, either
  - fix them (via PR's branching off the release branch) or
  - move them to another release milestone.
- After finalising the code, make sure all CI tests are passing.

### Documentation of changes since last release

- Create a changelog file in *changelog* directory. You may use git log, see [here](https://github.com/metno/pyaerocom/blob/master/changelog/CHANGELOG_v080_v0100.rst) for an example.
- Create a release summary, see [here](https://github.com/metno/pyaerocom/blob/master/changelog/v0100_release_summary.md) for an example (does not need to be a new file but can also be just specified in the provided text box when releasing on GitHub, see, e.g. [here]()). **NOTE**: You can use pycharm to compare diffs between 2 branches to see what are the main changes. Creating the release summary can be quite some work, but it is good to do it for documentation and also for a recap of what has actually happened since the last release.
- Check that version is correct (file *setup.cfg*). For instance, for release of version 1.0.0 it should be set to either 1.0.0 or 1.0.0.rcX where X denotes iterations of release candidates.

### Check code documentation

The PR for the release will automatically build the docs on ReadTheDocs (see Checks at the end of the PR). Please check and make sure the docs look alright.

## Publish release

- Merge release branch into master

### 1. Release on GitHub

- Go to https://github.com/metno/pyaerocom.
- Create a release and annotate the correct version (look for **Releases** on the right side).
- You may use the release summary as release text. If the release summary is rather extensive, you may also boil it down to the highlights and link to the release summary, but not needed really).
- Publish the release. This should automatically create a new zenodo DOI, check here:
  https://zenodo.org/record/4362479#.X9425NZ7kUE
  (Versions can be accessed on the right).
- You may want to check and update the info in the DOI (especially author names, etc).

**NOTE:** Even if you are very certain that everything is perfect and ready for the official release you may want to do the below steps first using a version that denotes a release candidate since once the assigned version (e.g. 1.0.0) is published on PyPi, there is no way to correct that version later (e.g. if you forgot to add a new dependency).

### 2. Publish on PyPi

- Make sure version on *setup.cfg* is correct
- Make sure there are no uncommited or unstaged changes in your local clone before running the next step, e.g. via:

    ``` bash
    git status .
    ```

- Install tools:  

    ``` bash
    python3 -m pip install -U pip pipx
    ```

    On the next steps we will use [build] to create a new [distribution package],
    [twine] to publish it to a [package index],
    and [pipx] to run each tool on an isolated environment.


    [pipx]: https://pypa.github.io/pipx
    [build]: https://pypa-build.readthedocs.io
    [twine]: https://twine.readthedocs.io
    [distribution package]: https://packaging.python.org/glossary/#term-Distribution-Package
    [package index]: https://packaging.python.org/glossary/#term-Package-Index

- Genereate new [distribution package]:

    ``` bash
    pipx run build
    ```

  This will create a *.tar.gz* and *.whl* in *dist/* dir.

- Check files

    ``` bash
    pipx run twine check dist/*
    ```

  Make sure the files are okay.

- Upload to pypitest:

    ``` bash
    pipx run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    ```

- Check that everything worked on test.pypi (link is provided in command line after uploading).

- Install locally from pypitest (the link is provided on the test.pypi website for the release).

- If everything works you can publish the official release on PyPi:

    ``` bash
    pipx twine upload dist/*
    ```

- ✨🌟✨You published the release as a pypi package✨🌟✨, try:

    ```bash
    pipx install pyaerocom==***version***
    ```

- **BUT**: you are almost there, but we also want to be able to install pyaerocom via conda (automatically with all requirements), so the beer has to wait !

### 3. Publish on conda-forge

- Fork [pyaerocom-feedstock](https://github.com/conda-forge/pyaerocom-feedstock) and clone your fork locally (if you have not already done so)
- Update *recipe/meta.yaml*
  - Update version
  - Update SHA256 key for your release. You can get it on PyPi:
    https://pypi.org/project/pyaerocom/*****version*****/#files
    Under **Hashes**, make sure you have the correct version here.
  - If the version has changed, set build number to 0.
  - Check if any requirements need to be updated.
- If *meta.yaml*  is in place, push to your remote fork.
- Go to [pyaerocom-feedstock](https://github.com/conda-forge/pyaerocom-feedstock) and create a PR.
- Follow all instructions and re-iterate if something is off. Else, merge PR.
- ✨🌟✨You published the release as a conda package✨🌟✨.

- **NOTE**: It may take a while (up to a day out of own experience) until the new version is available via

    ``` bash
    conda install -c conda-forge pyaerocom
    ```

- **But**: You can check if your version is available here:
  https://anaconda.org/conda-forge/pyaerocom
  or via `conda search -c conda-forge pyaerocom`
