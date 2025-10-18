@echo off

call .././setenv.bat
rem -- version the code
python job_versioning.py --appDirectory .././src

rem -- package the code
python job_package.py .././src

@echo on