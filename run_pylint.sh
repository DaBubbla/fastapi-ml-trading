#!/bin/bash

if python -c "import pylint" &> /dev/null; then
    echo 'pylint found...'
else
    echo 'installing pylint'
    pip install pylint
fi

pylint --rcfile=pylint.cfg src/
