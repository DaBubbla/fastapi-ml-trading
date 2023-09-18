import uvicorn
import os

os.environ["PYTHONASYNCIODEBUG"] = "1"
os.environ ["PYTHONDONTWRITEBYTECODE"]="1"

build_version = "0.0.0"

with open("./ci/version") as version_file:
    build_version = version_file.read().strip("\n")

os.environ["build_version"] = build_version
os.environ["run_local"] = "true"

from src.main.application import app

uvicorn.run(app, host="0.0.0.0", port=80)