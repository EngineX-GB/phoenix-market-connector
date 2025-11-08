rem In the Windows Command Prompt, execute this script from the deploy directory
rem not from the project root directory
rem Git/ Git Bash needs to be set to the PATH environment variable for this script to run properly.

@echo off

call .././setenv.bat
rem -- version the code
python job_versioning.py --appDirectory .././src

rem -- package the code
python job_package.py --src .././src

rem -- run pyinstaller to generate the executable
pyinstaller --onefile --add-data=.././src/app.json:. --add-data=.././src/template/config.properties.template:template --add-data=.././src/template/headers.json.template:template --name=market-connector .././src/portable-runner.py

rem -- package the binary into a zip
python job_package.py --binary .././src
