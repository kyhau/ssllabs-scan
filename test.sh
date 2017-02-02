#!/bin/bash
echo "TEST_BUILD: Create virtual env and install tox"
# Set to fail script if any command fails.
set -e
rm -rf env
virtualenv env
. env/bin/activate

echo "TEST_BUILD: Install dependencies for running tox, wheel and pytests"
pip install -r requirements-build.txt
# run the python tests
tox -r

# Leave virtual environment
deactivate
