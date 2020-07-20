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

# Translations
gettext:
	pybabel extract -F babel.cfg -o reddash/app/messages.pot .
	pybabel update -i reddash/app/messages.pot -d reddash/app/translations
upload_translations:
	crowdin upload sources
download_translations:
	crowdin download
compile_translations:
	pybabel compile -d reddash/app/translations