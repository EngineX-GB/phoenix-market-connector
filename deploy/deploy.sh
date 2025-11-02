#!/bin/sh
# Ensure that git is installed in linux for this to work

# -- run pyinstaller to generate the executable
pyinstaller --onefile --add-data=.././src/app.json:. --add-data=.././src/template/config.properties.template:template --add-data=.././src/template/headers.json.template:template --name=market-connector .././src/portable-runner.py

# -- package the binary into a zip
python job_package.py --binary .././src