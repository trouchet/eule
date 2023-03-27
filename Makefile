.PHONY: help clean test coverage docs servedocs install
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

rel_current_path = sys.argv[1]
abs_current_path = os.path.abspath(rel_current_path)
uri = "file://" + pathname2url(abs_current_path)

webbrowser.open(uri)
endef

export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef

export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"
DO_DOCS_HTML := $(MAKE) -C clean-docs && $(MAKE) -C docs html
SPHINXBUILD   = python3 -msphinx

PACKAGE_NAME = "eule"
PACKAGE_VERSION := poetry version -s

COVERAGE_IGNORE_PATHS = "eule/examples"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-cache clean-docs ## remove all build, test, coverage, Python artifacts, cache and docs

clean-docs: # remove docs for update
	rm -fr "docs/$$PACKAGE_NAME.rst" "docs/modules.rst" "docs/conftest.rst" "docs/examples.rst" "docs/tests.rst" "docs/_build" 

clean-build: # remove build artifacts
	rm -fr build/ dist/ .eggs/
	find . -name '*.egg-info' -o -name '*.egg' -exec rm -fr {} +

clean-pyc: # remove Python file artifacts
	find . -name '*.pyc' -o -name '*.pyo' -o -name '*~' -exec rm -rf {} +

clean-test: # remove test and coverage artifacts
	rm -fr .tox/ .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

test: ## run tests quickly with the default Python
	poetry shell
	pytest

test-watch: ## run tests on watchdog mode
	poetry shell
	ptw

lint: clean ## perform inplace lint fixes
	ruff --fix .
	pre-commit run --all-files

coverage: clean ## check code coverage quickly with the default Python
	coverage run --source "$$PACKAGE_NAME" -m pytest
	coverage report -m --omit="$$COVERAGE_IGNORE_PATHS"
	coverage html
	$(BROWSER) htmlcov/index.html

docs: clean ## generate Sphinx HTML documentation, including API docs
	poetry shell
	sphinx-apidoc -o "docs/" "$$PACKAGE_NAME" "tests" "examples" "conftest.py"
	$(MAKE) -C docs html
	$(BROWSER) 'docs/_build/html/index.html'

docs-watch: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$$DO_DOCS_HTML' -R -D .

install: clean ## install the package to the active Python's site-packages
	poetry shell
	poetry install

echo-version: ## echo current package version
	echo "v$$(poetry version -s)"

bump-version: ## bump version to user-provided {patch|minor|major} semantic
	poetry version $(v)
	git add pyproject.toml
	git commit -m "release/ tag v$$(poetry version -s)"
	git tag "v$$(poetry version -s)"
	git push
	git push --tags
	poetry version

publish: clean ## build source and publish package
	poetry publish --build

release: bump-version v=$(v) ## release package on PyPI
	$(MAKE) -C publish