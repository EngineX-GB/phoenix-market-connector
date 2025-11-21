@echo off

rem In the Windows Command Prompt, execute this script from the deploy directory
rem not from the project root directory
rem Git/ Git Bash needs to be set to the PATH environment variable for this script to run properly.

call .././setenv.bat

rem -- delete old build files
rmdir /s /q build
rmdir /s /q dist

rem -- version the code
python job_versioning.py --appDirectory .././src

rem -- package the code
python job_package.py --src .././src

rem -- run pyinstaller to generate the executable
pyinstaller --onefile --add-data=.././src/app.json:. --add-data=.././src/template/config.properties.template:template --add-data=.././src/template/headers.json.template:template --name=market-connector .././src/portable-runner.py

rem -- run pyinstaller to generate the executable (for the service version)
pyinstaller --onefile --add-data=.././src/app.json:. --add-data=.././src/template/config.properties.template:template --add-data=.././src/template/headers.json.template:template --hidden-import=uvicorn --hidden-import=fastapi --hidden-import=service-runner --name=market-connector-service .././src/service-runner.py

rem -- package the binary into a zip
python job_package.py --binary .././src

@echo on