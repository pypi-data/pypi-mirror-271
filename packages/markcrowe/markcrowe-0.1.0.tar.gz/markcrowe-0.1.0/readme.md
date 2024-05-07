
# [markcrowe.pypi](https://github.com/marcocrowe/markcrowe.pypi)

This package is published at <https://pypi.org/project/markcrowe/>

## Requirements

- [Python &GreaterEqual; 3.10.0](https://www.python.org/downloads/)

The packages in this archive are:

- data_analytics
- population_planning

## Install Python Package Builders

To install/upgrade Python packages to build a Python package run these commands:

```bash
pip install -r requirements.txt
```

```bash
pip install --upgrade pip
pip install --upgrade build
pip install --upgrade twine
```

In the event of an error, consider running the following commands:

```bash
python -m pip cache purge
python -m pip install -U pip
```

## Recommended IDEs

- [VS Code](https://code.visualstudio.com/): [`Python`](https://code.visualstudio.com/docs/languages/python)

## Build and publish a Python package

*All these commands must be run from the project root:*

### Update the required packages

To build the requirements.txt file run these commands:

```bash
pipreqs --force
```

### Build/rebuild the Python package

To build the Python package, run the following command:

```bash
python -m build
```

### Publish the Python package

To publish the package to PyPI, run the following command:

```bash
python -m twine upload dist/*
```

For username enter `__token__` and then your password.

The package is then available at [markcrowe](https://pypi.org/project/markcrowe/)

### Installation of the Python package

#### Remote installation

To install the package from [pypi.org](https://pypi.org), run the following command:

```bash
pip install markcrowe
```

#### Local installation

To install the package from local sources, run the following command:

```bash
pip install .\dist\markcrowe-0.1.0-py3-none-any.whl
```

To force a reinstall of the package from local sources, run the following command:

```bash
pip install .\dist\markcrowe-0.1.0-py3-none-any.whl --force-reinstall
```

Conda:

```bash
conda install .\dist\markcrowe-0.1.0-py3-none-any.whl --channel conda-forge
```

---
Copyright &copy; 2021 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
