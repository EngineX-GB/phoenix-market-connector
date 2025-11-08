: deploy.bat
: Saturday 8th November 2025
: This script will create the release artefacts
: Note, scm-config.properties must exist with the correct properties in the file.

@echo off

set "found=false"
set TAG_VERSION=%1
set WIN_DISTRO_FILE=%2
set LINUX_DISTRO_FILE=%3
set RELEASE_NOTES=%4
set RELEASE_TITLE=%5

set "CONFIG_FILE=scm-config.properties"
if not exist "%CONFIG_FILE%" (
    echo ERROR: Config file "%CONFIG_FILE%" not found. Please make sure it exists.
    goto :EOF
)

if not exist "%WIN_DISTRO_FILE%" (
    echo ERROR: "%WIN_DISTRO_FILE%" does not exist. Please make sure it exists. Aborting release.
    goto :EOF
)

if not exist "%LINUX_DISTRO_FILE%" (
    echo ERROR: "%LINUX_DISTRO_FILE%" does not exist. Please make sure it exists. Aborting release.
    goto :EOF
)


for /f "tokens=1,2 delims==" %%A in (%CONFIG_FILE%) do (
    if "%%A"=="GH_TOKEN" set "GH_TOKEN=%%B"
)



:: Loop through each line of output
for /f "delims=" %%A in ('gh --version') do (
    echo %%A | findstr /c:"gh version" >nul
    if %errorlevel% equ 0 (
        set "found=true"
    )
)

:: Check result
if "%found%"=="true" (
    echo Connect to Github CLI and releasing artefact
    :: Removed the gh auth login statement to see if it's needed is we are setting credentials in memory
    gh release create %TAG_VERSION% %WIN_DISTRO_FILE% %LINUX_DISTRO_FILE% --notes %RELEASE_NOTES% -t %RELEASE_TITLE%
) else (
    echo Could not detect Github CLI on build machine.
)

@echo on