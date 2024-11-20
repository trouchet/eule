.SILENT:
.PHONY: help clean test coverage docs servedocs install bump publish release
.DEFAULT_GOAL := help
SHELL := /bin/bash

UNAME := $(shell uname)
SED_CMD =
ifeq ($(UNAME), Darwin)
SED_CMD = sed -i ''
else
SED_CMD = sed -i
endif

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

BROWSER := python3 -c "$$BROWSER_PYSCRIPT"
DO_DOCS_HTML := $(MAKE) -C clean-docs && $(MAKE) -C docs html
SPHINXBUILD   = python3 -msphinx

PACKAGE_NAME = "eule"

COVERAGE_IGNORE_PATHS = "eule/examples"

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


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
	find . -name '*pycache*' -exec rm -rf {} +


test: ## run tests quickly with the default Python
	uv run pytest


watch: ## run tests on watchdog mode
	ptw .


search: ## Searchs for a token in the code. Usage: make search token=your_token
	grep -rnw . --exclude-dir=.venv --exclude-dir=.git --exclude=uv.lock -e "$(token)"


uv: ## install uv
	pip install uv


lint: clean ## perform inplace lint fixes
	uv run ruff --fix .


cov: clean ## Test coverages the source code 
	uv run coverage run --source "$$PACKAGE_NAME" --omit "tests/*,*/__init__.py" -m pytest --durations=10
	uv run coverage report -m


watch-cov: clean ## Checks code coverage quickly with the default Python
	find . -name '*.py' | entr -c make cov


docs: clean ## generate Sphinx HTML documentation, including API docs
	sphinx-apidoc -o "docs/" "$$PACKAGE_NAME" "tests" "examples" "conftest.py"
	$(MAKE) -C docs html
	$(BROWSER) 'docs/_build/html/index.html'


docs-watch: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$$DO_DOCS_HTML' -R -D .


env: ## Creates a virtual environment. Usage: make env
	uv venv


install: clean ## Installs the python requirements. Usage: make install
	uv sync


what: ## Lists all commits made since the last release commit with a tag pattern 'release/ tag vX.Y.Z'
	@LAST_RELEASE_COMMIT=$$(git log --oneline --grep="release/ tag v" -n 1 --pretty=format:"%H"); \
	if [ -z "$$LAST_RELEASE_COMMIT" ]; then \
		echo "Error: No release commit found with tag pattern 'release/ tag vX.Y.Z'."; \
		exit 1; \
	else \
		echo "Last release commit: $$LAST_RELEASE_COMMIT"; \
		git log --oneline "$$LAST_RELEASE_COMMIT..HEAD"; \
	fi


version: ## Echoes the package version
	@echo $$(grep '^version =' pyproject.toml | awk '{print $$3}' | tr -d '"')


next-version: ## Calculates the next version based on the bump type
	@if [ -z "$(v)" ]; then \
		echo "Error: Missing version bump type. Use: make next-version v={patch|minor|major}"; \
		exit 1; \
	fi; \
	\
	VALID_BUMPS="patch minor major"; \
	if ! echo "$$VALID_BUMPS" | grep -qw "$(v)"; then \
		echo "Error: Invalid bump type '$(v)'. Valid types are: $$VALID_BUMPS."; \
		exit 1; \
	fi; \
	\
	CURRENT_VERSION=$$($(MAKE) --silent version); \
	\
	MAJOR=$$(echo $$CURRENT_VERSION | cut -d '.' -f 1); \
	MINOR=$$(echo $$CURRENT_VERSION | cut -d '.' -f 2); \
	PATCH=$$(echo $$CURRENT_VERSION | cut -d '.' -f 3); \
	\
	if [ "$(v)" = "patch" ]; then \
		PATCH=$$((PATCH + 1)); \
	elif [ "$(v)" = "minor" ]; then \
		MINOR=$$((MINOR+1)); \
		PATCH=0; \
	elif [ "$(v)" = "major" ]; then \
		MAJOR=$$((MAJOR+1)); \
		MINOR=0; \
		PATCH=0; \
	fi; \
	\
	echo "$$MAJOR.$$MINOR.$$PATCH"


check-bump: ## Validates the version bump type
	@if [ -z "$(v)" ]; then \
		echo "Error: Missing version bump type. Use: make bump v={patch|minor|major}"; \
		exit 1; \
	fi

	@VALID_BUMPS="patch minor major"; \
	if ! echo "$$VALID_BUMPS" | grep -qw "$(v)"; then \
		echo "Error: Invalid version bump type '$(v)'. Valid types are: $$VALID_BUMPS."; \
		exit 1; \
	fi


bump: ## Bumps version to user-provided {patch|minor|major} semantic version
	@if [ -z "$(v)" ]; then \
		echo "Error: Missing version bump type. Use: make bump v={patch|minor|major}"; \
		exit 1; \
	fi; \
	$(MAKE) check-bump v=$(v); \
	NEW_VERSION=$$($(MAKE) --silent next-version v=$(v)); \
	if [ "$(dry-run)" = "true" ]; then \
		echo "Dry run: Version would be bumped to $$NEW_VERSION"; \
		exit 0; \
	fi; \
	NEXT_VERSION=$$($(MAKE) --silent next-version v=$(v)); \
	\
	# Update the version in pyproject.toml \
	sed -i "s/^version = \".*\"/version = \"$$NEXT_VERSION\"/" pyproject.toml; \
	uv lock; \
	git add pyproject.toml uv.lock; \
	git commit -m "release: tag v$$NEW_VERSION"; \
	git tag "v$$NEW_VERSION"; \
	git push --tags;\
	echo "Package tagged to version $$NEW_VERSION";


publish: clean ## Builds source and publish package
	uv build
	uv publish


release: ## Releases package on PyPI
	@if [ -z "$(v)" ]; then \
		echo "Error: Missing version bump type. Use: make release v={patch|minor|major}"; \
		exit 1; \
	fi; \
	$(MAKE) bump v=$(v); \
	$(MAKE) publish


requirements: ## Generates minimal requirements. Usage: make requirements
	python3 scripts/clean_packages.py requirements.txt requirements.txt
	python3 scripts/clean_packages.py requirements_dev.txt requirements_dev.txt
