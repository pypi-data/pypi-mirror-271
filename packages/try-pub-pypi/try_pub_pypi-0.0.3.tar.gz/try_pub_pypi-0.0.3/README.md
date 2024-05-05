[![Publish Python 🐍 distribution 📦 to PyPI and TestPyPI](https://github.com/seralekseenko/try_pub_pypi/actions/workflows/pub_on_pypi_org.yml/badge.svg)](https://github.com/seralekseenko/try_pub_pypi/actions/workflows/pub_on_pypi_org.yml)

[![Lint & Tests](https://github.com/seralekseenko/try_pub_pypi/actions/workflows/lint_test.yml/badge.svg)](https://github.com/seralekseenko/try_pub_pypi/actions/workflows/lint_test.yml)

# try_pub_pypi

Only test to automate publishing to pypi.org

### virtual python3 ENV

1. Create virtual ENV → `python3 -m venv .venv` # смотри conda (Anaconda)
2. Activate → `source .venv/bin/activate`
3. Check virt env → `echo $VIRTUAL_ENV` → should be non empty output
4. Deactivate → `deactivate` or reopen terminal session

### Requirements

- instal `pip install -r requirements.txt`
- save `pip freeze > requirements.txt`
- check to old requirements `pip list --outdated`
- upgrade some package `pip install -U package_name`

### Run tests

A simple way: `python3 -m unittest discover -s ./tests` or `pytest`

### Publish on pypi.org

- manual mod: just run Actions → Publish Python 🐍 distribution 📦 to PyPI
- pub by special commit tag to only 'main' branch:
    1. `git commit -m "your important message"` & `git push`
    2. `git tag vx.x.x`; `x` is the numbers! Follow the pattern: 'v[0-9]+.[0-9]+.[0-9]+'
    3. `git push origin vx.x.x`
