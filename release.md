# how to create a new release and publish to pypi

## update setup.py

in particular, update the version tag and perhaps the Development Status classifier.

## create a new release on GitHub

Go to https://github.com/varkenvarken/gentrypy and select "Create a new release".

Let the release tag reflect the version in setup.py 

Creating the release will trigger a workflow that will build the /dist with setuptools
and publish the new version of the package to pypi.

The pypi project https://pypi.org/project/gentry/ has been set up for trusted publisher management againts the GitHub repo.

The GitHub action was pinned against the SHA-1 commit hash for https://github.com/pypa/gh-action-pypi-publish/releases/tag/v1.12.4

## publish a pypi package with twine

See /bin/pypi for a script that does that. It need twine (apt install twine) and an access token in ~/.pypirc
