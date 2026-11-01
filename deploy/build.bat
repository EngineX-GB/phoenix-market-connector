@echo off

rem In the Windows Command Prompt, execute this script from the deploy directory
rem not from the project root directory
rem Git/ Git Bash needs to be set to the PATH environment variable for this script to run properly.

call .././setenv.bat

if not exist "%PYTHON_HOME%" (
    echo ERROR: "%PYTHON_HOME%" does not exist. Please make sure it exists. Aborting release.
    goto :EOF
)

rem -- delete old build files
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

echo "Install dependencies"

pip install beautifulsoup4==4.12.3 --no-input
pip install requests==2.31.0 --no-input
pip install cloudscraper==1.2.71 --no-input
pip install uvicorn==0.35.0 --no-input
pip install fastapi==0.116.1 --no-input
pip install fastapi-cli==0.0.8 --no-input
pip install fastapi-cloud-cli==0.1.5 --no-input
pip install python-multipart==0.0.20 --no-input
pip install pyinstaller==6.15.0 --no-input
pip install pyinstaller-hooks-contrib==2025.8 --no-input


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