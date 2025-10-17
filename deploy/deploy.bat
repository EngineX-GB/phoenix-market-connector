@echo off

call .././src/setenv.bat
rem -- version the code
python job_versioning.py --appDirectory .././src

rem -- packge the code
python job_package.py .././src

@echo on