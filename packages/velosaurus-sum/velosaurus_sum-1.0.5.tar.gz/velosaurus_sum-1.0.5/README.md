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
