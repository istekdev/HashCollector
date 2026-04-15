#!/bin/bash

set -e

cd "$(dirname "$0")/.."

pyinstaller --onefile --name HashCollector --add-data "config.json:." --add-data "components;components" --add-data "integrity;integrity" --distpath "output/dist" --workpath "output/build" --specpath "output/spec" core.py
