# Dummy Python DevOps Project

## Prerequisites

### Setup Python Environment

```bash
# Create/activate/deactivate venv
python -m venv venv
.\venv\Scripts\activate
source venv/bin/activate
.\venv\Scripts\deactivate

# Install packages with activated env and check
python -m pip install --upgrade pip
pip install --upgrade -r ./requirements.txt 
pip list

# Freeze and Upgrade current packages  
pip freeze > pip_list.txt   
pip install --upgrade --force-reinstall -r requirements.txt
```

## Unit Testst

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Generate and test python package locally

```bash
python setup.py sdist bdist_wheel
pip install dist/velosaurus_sum-1.0.4-py3-none-any.whl
python .\src\test_package\test.py  
```

## Tools

- ruff (linter, formatter)
- mypy (type annotation linter)
  - if **Extension** installed, add rule: Search for mypy in Settings and ad "Mypy-type-checker args": ``"python.linting.mypyArgs": [     "--ignore-missing-imports" ]``
- autoDocstring - Python Docstring Generator
- Jupyter and Python plugins

Further:

- pytest
- coverage
- pre-commit

### ruff and mypy

Tools can be applied manualle in console or automatically in pipeline on commit/PR. Configuration for manual/local usage is done in **settings.json**. Configuration for pipeline/build-tool usage is done via **pyproject.toml**.

Use Ruff instead of flake8 (linter), black (formatter) and isort (import sorter) separately.

- in root foler: `python .\run_ruff.py`

- **ruff** (linter / formatter)
  - `ruff check .`   ...basic check (linter)
  - `ruff check --fix .` ...fix basic issues (linter)
  - `ruff format --diff .` (show diffs)
  - `ruff format --check .` (show files)
  - `ruff format .` (apply formatter)

- **mypy** (static type annotations)
  - `mypy --exclude venv .`
