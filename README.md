# Copier PyPI Sphinx Github Actions

## Overview

This repo is a template to use for starting a new Python package
which is hosted on PyPi and uses Sphinx for documentation
hosted on Github pages. It has a built-in CI/CD system using Github Actions.
for features and setup. The CI system has
the following features:

- Runs any tests in `tests` with `pytest`
- Lints code using `flake8`
- Static code checks with `mypy`
- Deploys PyPI package and creates corresponding Github release
- Deploys Sphinx documentation on Github Pages
  - Autodoc/autosummary already set up
  - Automatic sitemap.xml generated
  - Just add Google Analytics ID to enable tracking
  - Read the Docs Theme with Custom CSS
  - Notebook-style examples with Sphinx Gallery complete with download and Binder links
    - Auto-converts Jupyter notebooks in `nbexamples`
- Convenient CLI interface to normal development tasks using [`nox`](https://nox.thea.codes/en/stable/)
- Automatically creates release notes based on merged pull requests
  once a commit is done to master with the version changed in `conf.py`
- Syncs new changes from the copier template using Flexlate
  on a cron workflow. Creates a PR with the changes to be merged
  manually. Creates an issue if it is not possible to commit the changes (when there are
  changes to workflow files).
- Collects TODO comments and converts them into issues
- Closes TODO issues once comments are removed
- Caches dependencies for faster builds

See
[the example generated repo](https://github.com/nickderobertis/pypi-sphinx-flexlate-example).

## Getting Started

### Create Project from Copier using Flexlate

Install [Flexlate](https://github.com/nickderobertis/flexlate)
if you haven't installed it yet:

    pip install flexlate

Generate a Python package project:

    fxt init-from https://github.com/nickderobertis/copier-pypi-sphinx-flexlate

### Create git repo

Create the git repo and push to Github.

### Adding Secrets

Go into the repo settings, under Secrets, and add the following secrets:

- `pypi_password`: Personal token for PyPI
- `gh_token`: Github personal access token
- `CODECOV_TOKEN` (optional): [codecov.io](https://codecov.io) token for this project

### `conf.py`

Edit `conf.py` in the main repo directory. This contains the main
settings for the PyPi package. The settings should be mostly filled out
from using Flexlate, but specific package details such as dependencies
still need to be added.

### Automatic Templates Updates via CI

Enable automatic updates of the templates via CI by adding the official [Flexlate Github Actions template](https://github.com/nickderobertis/copier-flexlate-github-actions):

```shell
fxt add source https://github.com/nickderobertis/copier-flexlate-github-actions
fxt add output copier-flexlate-github-actions
```

### Adding Project Source

Add your project code to the folder named by `PACKAGE_NAME`.

### Adding Global Requirements to Build

If you do not already have `pipenv` installed, you will need to run:

```
pip install pipenv
```

Then regardless of whether you already had `pipenv` installed, you will
need to navigate to the repo folder and run:

```
pipenv update
```

### Setting up Documentation

Edit `docsrc/source/index.rst` to add some information about your package.

Edit `docsrc/source/tutorial.rst` to put your own tutorial, or remove it
and remove it from the `toctree` directive in `docsrc/source/index.rst`.

You may further modify Sphinx configuration in `docsrc/source/conf.py`
if you wish.

Add [Sphinx Gallery](https://sphinx-gallery.github.io/stable/index.html) examples
in the `examples` folder. You can also add Jupyter notebook examples in the
`nbexamples` folder, and they will automatically be converted to
Sphinx Gallery-style examples and included with `examples` in the
build of the documentation.

### Commit and Push

After the preceding steps, now commit your changes and push to `master`
if not done already. After a few minutes, Github Actions should create
a `gh-pages` branch which has the documentation HTML in it.

### Check Labels

The following labels are used in the CI/CD. They should have been added in Labels in the
repo settings after the Github Actions from the first push have
finished running:

- `no auto merge`: added to prevent automatic merging of
  pull requests by maintainers
- `maintenance`: one of the output categories for release notes
- `automated pr`: Used by automated template update cron workflow which
  uses Flexlate to check for changes in the template and opens a PR
  automatically if so.
- `automated issue`: Due to limitations in Github Actions, the template update
  cron workflow is not able to commit to the repo if the changes include changes to
  workflow files. It instead raises an issue to update the template in this case. This
  label is applied to these issues as well as the `maintenance` label.

### Github Pages Setup

Note: This should happen automatically after Github Actions creates
the `gh-pages` branch. But follow these steps if your docs still do
not work.

Go to repo settings, Github Pages section. For the Source dropdown,
select "gh-pages branch". The settings page should reload,
and in the Github Pages section it should show the URL of your
documentation. You should be able to see the documentation at the URL
after a few seconds, but it will still be the example documentation.

If "gh-pages branch" is not shown in the dropdown, you need to make one
release commit and push it, so that the `gh-pages` branch will be added
to your repo. After doing that, you can go into the repo settings
and select "gh-pages branch" as described.

### Optional Steps

#### Set Master to Protected Branch

It is recommended to make master a protected branch so that nobody can
delete it.

#### Setup Codecov

Go to [codecov.io](https://codecov.io), log in via Github, click Repositories then
"Add new repository" and select this repository from the list. Copy the
token for Codecov to use in the next step.

## Built-in CI/CD

### On Every Push

Github Actions are used to automatically run the following steps on every push:

- Check Python syntax with `flake8`
- Run `pytest`
- Static typing checks with `mypy`

### When Branch is `master`

If the branch is the `master` branch, then it will also:

- Upload `pytest` results to `codecov`

#### If there is a change in `docsrc`

If the branch is the master branch, and there was a change in `docsrc`, it will do
all the steps in On Every Push and When Branch is `master`, then it will:

- Build documentation HTML using Sphinx
- Create `gh-pages` branch and copy HTML there
- Push to `gh-pages` branch, which will update the hosted documentation

#### If there is a change in the package version

If the branch is the master branch, and there was a change in the package version
in `conf.py`, it will do
all the steps in On Every Push and When Branch is `master`, then it will:

- Build documentation HTML using Sphinx
- Create `gh-pages` branch and copy HTML there
- Push to `gh-pages` branch, which will update the hosted documentation
- Build Python package
- Upload Python package to PyPI
- Create a Github release pointing to any merged pull requests since
  the last version bump

### If a Pull Request is Opened

The CI/CD system will check whether the pull request was opened by a maintainer
(configured in conf.py). If so, it will auto-merge the pull request after
it has passed CI checks. It will then run the deployment pipeline. To avoid
this auto-merge behavior, add the label "no auto merge" to the pull request.

## Regular Usage

Once everything is set up, just commit your changes. The built-in
CI/CD will take care of testing, build, and deployment of PyPI package
and documentation. If you use pull requests on Github then it will
show you whether it passes the CI tests.

## Local Usage

Building the documentation locally makes sense if you are
updating it but don't want to make it live yet. You can view
the HTML files in the `docs` folder via a browser after building them.

### Building Documentation

Navigate into the `docsrc` folder and run:

```
pipenv run make github
```

This should generate documentation HTML in the `docs` folder.

For development, get an auto-reloading development server by running:

```shell
pipenv shell
cd docsrc
./dev-server.sh
```

### Uploading to PyPi

Navigate to the repo base folder and run:

```
pipenv run python upload.py
```

### Updating Build Requirements

The Github Actions CI/CD uses `Pipfile.lock` to install its
requirements. Run `pipenv update` locally to update the
`Pipfile.lock` with the newest dependencies and push into
the `master` branch to get the dependencies updated
on the CI/CD system.

### Syncing with the `copier` template

There is a built-in workflow which runs daily to check for
updates in the `copier` template. If it finds an update,
it will use Flexlate to apply the update and raise a PR with the
changes. Manually review the changes, adjusting if needed, then
merge the PR to keep updated with the template.

## Links

See
[the example generated repo](https://github.com/nickderobertis/pypi-sphinx-flexlate-example)

## Development Status

This project uses [semantic-release](https://github.com/semantic-release/semantic-release) for versioning.
Any time the major version changes, there may be breaking changes. If it is working well for you, consider
pegging to the current major version, e.g. `copier-pypi-sphinx-flexlate@v1`, to avoid breaking changes. Alternatively,
you can always point to the most recent stable release with the `copier-pypi-sphinx-flexlate@latest`.

## Developing

Clone the repo and then run `npm install` to set up the pre-commit hooks.

## Author

Created by Nick DeRobertis. MIT License.
