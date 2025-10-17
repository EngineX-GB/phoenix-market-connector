@echo off
call setenv.bat
title phoenix-connector-service
SET FLASK_APP=ServiceRunner
@echo on
flask run