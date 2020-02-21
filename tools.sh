#!/usr/bin/env bash
################################################################################
current_path=$(pwd)
################################################################################
echo ""
echo "Folder: $current_path"
echo ""
################################################################################
echo "Run PyLint for test code."
pylint3 -s y tests
################################################################################
echo "Run tests..."
python3 -m unittest discover tests "*_test.py"
################################################################################
echo "Generate code documentation..."
pdoc3 --html --output-dir docs/tests --force jsonsimpleconfig
################################################################################
echo "Generate tests documentation..."
pdoc3 --html --output-dir docs/tests --force tests
################################################################################
echo ""
################################################################################