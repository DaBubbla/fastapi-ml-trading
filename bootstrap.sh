#!/usr/bin/env sh

pwd
cd /app
pwd
python --version
pip install --no-cache-dir -r requirements.txt --upgrade

echo "App directory:"
ls -lrt .
echo "Pip Dependencies installed:"
pip list
