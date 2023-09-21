#!/bin/bash
set -x

export build_version="$(<ci/version)"
export run_local="true"

#TODO: might add a switch to run local or via linode

export stage="dev"

uvicorn --host 0.0.0.0 --port 80 src.main.application:app --reload --workers 2