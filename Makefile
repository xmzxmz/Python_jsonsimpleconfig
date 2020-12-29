###############################################################################
# Setup
###############################################################################

CURRENT_DIRECTORY := $(shell pwd)
# SHELL:=/bin/bash
target: help;

###############################################################################
# Bundles
###############################################################################

lint: pylint pycodestyle flake8
test: unittest pytest
test-tox: unittest pytest tox
clean: clean-pyc clean-build clean-cache clean-docs clean-tox
doc: doc-jsc doc-tests
ps: vc-pipeline-scan

all: init lint test doc clean
.PHONY : all

###############################################################################
# Init package
###############################################################################
help:
	@echo "-------------------------------------------------------------------"
	@echo "    lint"
	@echo "        Run all linters."
	@echo "    pylint"
	@echo "        Run pylint."
	@echo "    pycodestyle"
	@echo "        Run pycodestyle."
	@echo "    flake8"
	@echo "        Run flake8."
	@echo "-------------------------------------------------------------------"
	@echo "    test"
	@echo "        Run all tests."
	@echo "    unittest"
	@echo "        Run unittest."
	@echo "    pytest"
	@echo "        Run pytest."
	@echo "-------------------------------------------------------------------"
	@echo "    clean"
	@echo "        Run clean."
	@echo "    clean-pyc"
	@echo "        Run clean-pyc."
	@echo "    clean-build"
	@echo "        Run clean-build."
	@echo "-------------------------------------------------------------------"
	@echo "    doc"
	@echo "        Run documentation."
	@echo "    doc-jsc"
	@echo "        Run documentation for JSC."
	@echo "    doc-tests"
	@echo "        Run documentation for tests."
	@echo "-------------------------------------------------------------------"
	@echo "    init"
	@echo "        Install dependencies."
	@echo "-------------------------------------------------------------------"
	@echo "    all"
	@echo "        Run everything."
	@echo "-------------------------------------------------------------------"

###############################################################################
# Init package
###############################################################################
init:
	pip install -r requirements.txt

###############################################################################
# PyLint
###############################################################################
pylint:
	@echo "Run PyLint ..."
	@eval pylint -s y --rcfile=.pylintrc setup.py
	@eval pylint -s y --rcfile=.pylintrc jsonsimpleconfig
	@eval pylint -s y --rcfile=.pylintrc tests

###############################################################################
# Py Code Style
###############################################################################
pycodestyle:
	@echo "Run PyCodeStyle ..."
	@eval pycodestyle --config=.pycodestyle setup.py
	@eval pycodestyle --config=.pycodestyle jsonsimpleconfig
	@eval pycodestyle --config=.pycodestyle tests
	@eval pycodestyle --config=.pycodestyle .

###############################################################################
# Flake8
###############################################################################
# @eval flake8 --count --show-source --statistics --benchmark --bug-report .
###############################################################################
flake8:
	@echo "Run flake8 ..."
	@eval flake8 setup.py
	@eval flake8 jsonsimpleconfig
	@eval flake8 tests
	@eval flake8
	@eval flake8 --exclude=jsonsimpleconfig --exclude=tests
	# Flake8 stats
	@eval flake8 --count --statistics --benchmark .

###############################################################################
# Tox
###############################################################################
tox:
	@echo "Run Tox ..."
	@eval tox

###############################################################################
# Run unit tests
###############################################################################
unittest:
	@echo "Run unit tests..."
	@eval python3 -m unittest discover tests "*_test.py"

###############################################################################
# Run py3 tests
###############################################################################
pytest:
	@echo "Run py3 tests..."
	@eval pytest --ignore=test --ignore=jsonsimpleconfig tests

###############################################################################
# Clean tools
###############################################################################
clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean-tox:
	rm --force --recursive .tox/
	rm --force --recursive htmlcov/
	rm --force .coverage
	rm --force coverage.xml
	rm --force junit.xml

clean-cache:
	rm --force --recursive .cache/
	rm --force --recursive .pytest_cache/

clean-docs:
	rm --force --recursive docs/tests/

###############################################################################
# Run documentation
###############################################################################
doc-jsc:
	@echo "Run documentation jsc..."
	@eval pdoc3 --html --output-dir docs/tests --force jsonsimpleconfig

doc-tests:
	@echo "Run documentation tests..."
	@eval pdoc3 --html --output-dir docs/tests --force tests

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
	@$(eval JAVA_OPTIONS=)
	@$(eval PIPELINE_SCAN='pipeline-scan-LATEST/pipeline-scan.jar')
	@$(eval TEST_FILE=jsc.tgz)
	@$(eval cmd="${JAVA} ${JAVA_OPTIONS} -jar ${PIPELINE_SCAN} -vid ${VERACODE_API_ID} -vkey ${VERACODE_API_KEY} -f ${TEST_FILE} -so true --issue_details true -p jsonsimpleconfig -ds Release")
	@cd ${SCAN_FOLDER} && eval $(cmd)

###############################################################################
#                                End of file                                  #
###############################################################################
