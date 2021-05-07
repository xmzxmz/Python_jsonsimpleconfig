###############################################################################
# Setup
###############################################################################

CURRENT_DIRECTORY := $(shell pwd)
# SHELL:=/bin/bash
target: help;

###############################################################################

.DEFAULT_GOAL := help
SOURCE_DIR=jsonsimpleconfig

UNAME=$(shell uname -s)

# If TOX is not installed we make this a dependency
ifeq ($(shell which tox),)
    TOX=tox
endif

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

###############################################################################
# Bundles
###############################################################################

lint: pylint pycodestyle flake8 mypy black  ## Run all linters.
test: unittest pytest doctest  ## Run all tests
test-tox: unittest pytest tox ## Run tox tests
clean: clean-pyc clean-build clean-cache clean-docs clean-tox ## Run clean all
doc: doc-jsc doc-tests  ## Run docs
ps: vc-pipeline-scan  ## Run Veracode pipeline-scan

all: init lint test doc clean ## Run everything.
.PHONY : all

###############################################################################
# Init package
###############################################################################
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

tox-install: ## install the tox package
	pip install tox

install: clean ## install the package to the active Python's site-packages
	pip install poetry
	poetry export -f requirements.txt -o requirements.txt --dev --without-hashes
	poetry install

###############################################################################
# Init package
###############################################################################

init: install ## Install dependencies.

###############################################################################
# PyLint
###############################################################################
pylint: ## Run pylint.
	@echo "Run PyLint ..."
	@eval pylint -s y --rcfile=.pylintrc jsonsimpleconfig
	@eval pylint -s y --rcfile=.pylintrc tests

###############################################################################
# Py Code Style
###############################################################################
pycodestyle:  ## Run pycodestyle
	@echo "Run PyCodeStyle ..."
	@eval pycodestyle --config=.pycodestyle jsonsimpleconfig
	@eval pycodestyle --config=.pycodestyle tests
	@eval pycodestyle --config=.pycodestyle .

###############################################################################
# Black code style
###############################################################################
black: ## Runs black on the source for PEP8 compliance
	black $(SOURCE_DIR) tests

###############################################################################
# Flake8
###############################################################################
# @eval flake8 --count --show-source --statistics --benchmark --bug-report .
###############################################################################
flake8: ## Run flake8.
	@echo "Run flake8 ..."
	@eval flake8 jsonsimpleconfig
	@eval flake8 tests
	@eval flake8
	@eval flake8 --exclude=jsonsimpleconfig --exclude=tests
	# Flake8 stats
	@eval flake8 --count --statistics --benchmark .

###############################################################################
# MyPy
###############################################################################
mypy:
	@echo "Run mypy ..."
	@eval mypy jsonsimpleconfig

###############################################################################
# Tox
###############################################################################
tox: ## Run Tox.
	@echo "Run Tox ..."
	@eval tox

###############################################################################
# Run unit tests
###############################################################################
unittest:  ## Run unittest.
	@echo "Run unit tests..."
	@eval python3 -m unittest discover tests "*_test.py"

###############################################################################
# Run py3 tests
###############################################################################
pytest:  ## Run pytest.
	@echo "Run py3 tests..."
	@eval pytest --ignore=test --ignore=jsonsimpleconfig tests

###############################################################################
# Run doctests
###############################################################################
doctest:  ## Run doctest.
	@echo "Run doctests..."
	@eval pytest --doctest-modules $(SOURCE_DIR)

doctest-verbose:  ## Run doctest verbose.
	@echo "Run doctests verbose..."
	@eval python -m doctest $(SOURCE_DIR)/*.py -v

###############################################################################
# Clean tools
###############################################################################
clean-pyc:  ## Run clean-pyc."
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-build:  ## Run clean-build."
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean-tox:  ## Run clean-tox."
	rm --force --recursive .tox/
	rm --force --recursive htmlcov/
	rm --force .coverage
	rm --force coverage.xml
	rm --force junit.xml
	rm --force requirements.tox.txt
	rm --force requirements.txt

clean-cache:   ## Run clean-cache."
	rm --force --recursive .cache/
	rm --force --recursive .pytest_cache/
	rm --force --recursive .mypy_cache/

clean-docs:  ## Run clean-docs."
	rm --force --recursive docs/tests/

###############################################################################
# Run documentation
###############################################################################
doc-jsc:  ## Run documentation for jsc.
	@echo "Run documentation jsc..."
	@eval pdoc3 --html --output-dir docs/tests --force jsonsimpleconfig

doc-tests:  ## Run documentation for tests.
	@echo "Run documentation tests..."
	@eval pdoc3 --html --output-dir docs/tests --force tests

###############################################################################
# Build dist
###############################################################################
build: clean lint  ## build python package.
	@echo "Run build..."
	@eval poetry export -f requirements.txt -o requirements.txt --dev --without-hashes
	@eval poetry build

###############################################################################
# Pipeline scan (Veracode)
###############################################################################
vc-pipeline-scan:
	@pwd
	@$(eval SCAN_FOLDER=.pipeline-scan-workspace)
	@echo "--------------------------"
	@if [ -d ${SCAN_FOLDER} ]; then rm -rf ${SCAN_FOLDER}; fi
	@mkdir -p ${SCAN_FOLDER}
	@echo "====================="
	@echo "Run Pipeline scan ..."
	@echo "====================="
	@echo "Prepare source package ..."
	@echo "--------------------------"
	tar czf "${SCAN_FOLDER}/jsc.tgz" jsonsimpleconfig
	@cd ${SCAN_FOLDER} && pwd && ls -lah
	@echo "Prepare pipelinescan ..."
	@echo "------------------------"
	wget https://downloads.veracode.com/securityscan/pipeline-scan-LATEST.zip -P "${SCAN_FOLDER}"
	@unzip -d "${SCAN_FOLDER}/pipeline-scan-LATEST" "${SCAN_FOLDER}/pipeline-scan-LATEST.zip"
	@rm "${SCAN_FOLDER}/pipeline-scan-LATEST.zip"
	@echo "Execute scan ..."
	@echo "----------------"
	@$(eval JAVA=java)
	@$(eval PIPELINE_SCAN='pipeline-scan-LATEST/pipeline-scan.jar')
	@$(eval TEST_FILE=jsc.tgz)
	@$(eval cmd="${JAVA} ${JAVA_OPTIONS} -jar ${PIPELINE_SCAN} -vid ${VERACODE_API_ID} -vkey ${VERACODE_API_KEY} -f ${TEST_FILE} -so true --issue_details true -p jsonsimpleconfig -ds Release")
	@cd ${SCAN_FOLDER} && eval $(cmd)

###############################################################################
#                                End of file                                  #
###############################################################################
