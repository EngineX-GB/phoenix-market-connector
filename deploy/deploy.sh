#!/bin/sh

# delete the build and dist folders in preparation for a clean build
rm -rf build
rm -rf dist

# -- run pyinstaller to generate the executable
pyinstaller --onefile --add-data=.././src/app.json:. --add-data=.././src/template/config.properties.template:template --add-data=.././src/template/headers.json.template:template --name=market-connector .././src/portable-runner.py

cp .././src/run.sh ./dist

# -- package the binary into a zip
python job_package.py --binary .././src