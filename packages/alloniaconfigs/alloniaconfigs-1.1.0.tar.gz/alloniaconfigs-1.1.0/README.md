# Public Project AllOnIAConfigs

This project contains the :obj:`~alloniaconfigs.configs.Configs` class that allows the user to
easily handle configurations.

You can find the user documentation [this URL](https://aleia-team.gitlab.io/public/alloniaconfigs)

This is a public project. Everyone is welcome to contribute to it.

## Installation

```bash
pip install alloniaconfigs
````

## Contributing

This is an open-source project. Everyone is welcome to contribute to it. To do
so, fork the repository, add your features/fixes on your forked repository,
then open a merge request to the original repository.

### Install dependencies using poetry

This project uses [Poetry](https://python-poetry.org/) to manage its
working environment. Install it before coding in project.

Then, run 

 ```bash 
poetry env use python3.12
poetry install
poetry run pre-commit install
```

### Testing

```bash
poetry run pytest tests # Parallelized
poetry run pytest tests -n 0 # Sequential

# Sequential with logs (logs can't work with parallelized tests)
poetry run pytest tests -n 0 -s # -s is the equivalent of --capture=no
```

#### Coverage

We use `pytest-cov` to display the coverage, so, after run
tests you can check the reports (term, html, xml are enabled), if you want to
improve your coverage, the better thing to do is to check the html report in
your browser:

```bash
open htmlcov/index.html
```

### Lint

To run the linters used by this project, you can run:
```bash
poetry run pre-commit run # Run lint only on staged files

# Manually check conventional commits format:
poetry run pre-commit run gitlint --hook-stage commit-msg --commit-msg-filename .git/COMMIT_EDITMSG
```

### User documentation

The documentation source files are located in [here](docs/source/). If you add
new features, please add them to the documentation as well.

You can buid the documentation locally by doing

```bash
cd docs
make html
```

The produced documentation should then be readable by opening the file in
docs/build/html/index.html in a web browser.
