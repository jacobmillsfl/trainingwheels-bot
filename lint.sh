#!/bin/bash
#
# Performs linting on the solution using rules defined in the .pylintrc file
pylint --rcfile=.pylintrc $(git ls-files '*.py')
