# ~
#
# Makefile for managing development
#
# ------------------------------------------------------


# config
# -----
PROJECT     = `grep 'name *= *' setup.cfg | sed 's/.*=//g' | tr -d '[:space:]'`
VERSION     = `git show -s --format="%cd-%h" --date=format:'%Y.%m.%d'`

requirements: init ## install all requirements for using repository
	python -m pip install -r requirements.txt

test: ## run testing suite for module using py.test
	py.test

