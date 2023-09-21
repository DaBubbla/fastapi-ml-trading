#!/bin/bash

if python -c "import pytest" &> /dev/null; then
    echo 'pytest found...'
else
    echo 'installing pytest'
    pip install pytest pytest-cov
fi

export run_local="true"

pytest --cov-config=pytest.ini --cov=. --cov-report=term-missing

unset run_local