PYTHON ?= python3.8

# Python Code Style
reformat:
	$(PYTHON) -m black -l 99 reddash
stylecheck:
	$(PYTHON) -m black --check -l 99 reddash
stylediff:
	$(PYTHON) -m black --check --diff -l 99 reddash

# Development environment
newenv:
	$(PYTHON) -m venv --clear .venv
	.venv/bin/pip install -U pip setuptools