"""
Name:           job_package.py
Description:    To package the versioned release of the core component
Date:           2022-11-27

Usage:

args:
    functionType    [required]      whether the script should package the source or package the pyinstaller binary
    appDirectory    [required]      the directory of the app (to be packaged) that contains the app.json file

python job_package.py <function type> <appDirectory_containing_the_app.json_file>

e.g.

python job_package.py --src .././src

python job_package.py --binary .././src

"""

import os
import datetime
import shutil
import sys
import job_versioning as jobVersion

CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
WINDOWS_OS_NAME = "nt"


# Note: If you want this script to be used for other apps, then the CODE_DIRECTORY and APPLICATION_CONFIG
# will need to be generic.
# Also implies that the app's directory must have an app.json file in it.


def zip(directoryPath, destinationPath, applicationName, applicationVersion):
    return shutil.make_archive(destinationPath + "/" + applicationName + "_" + applicationVersion, "zip", directoryPath)


def create_version_file(directoryPath, versionNumber):
    f = open(directoryPath + "/version.txt", 'w', encoding='utf-8')
    f.write(versionNumber)
    f.close()

def check_os_name():
    if os.name == WINDOWS_OS_NAME:
        return "windows"
    else:
        return "linux"

def get_binary_extension():
    if os.name == WINDOWS_OS_NAME:
        return ".exe"
    else:
        return "";

if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("[ERROR] Enter the required arguments")
        exit(1)

    # what to do (e.g. "--src" for packaging the source or --binary for packaging the binary)
    FUNCTION_PARAMETER = sys.argv[1]
    CODE_DIRECTORY = sys.argv[2]
    DISTRO_DIRECTORY = "./distro"
    APPLICATION_CONFIG = jobVersion.readConfig(CODE_DIRECTORY)
    APPLICATION_NAME = APPLICATION_CONFIG["application"]
    APPLICATION_VERSION = APPLICATION_CONFIG["version"]

    if not os.path.exists(DISTRO_DIRECTORY):
        print("[ERROR] " + DISTRO_DIRECTORY + " does not exist")
        os.makedirs(DISTRO_DIRECTORY, exist_ok=True)
    if not os.path.exists(CODE_DIRECTORY):
        print("[ERROR] " + CODE_DIRECTORY + " does not exist")
        sys.exit(1)

    if FUNCTION_PARAMETER == "--src":
        result = zip(CODE_DIRECTORY, DISTRO_DIRECTORY, APPLICATION_NAME, APPLICATION_VERSION)
        if result is not None:
            create_version_file(DISTRO_DIRECTORY, APPLICATION_VERSION)
            print("[INFO] " + result + " is generated")

    elif FUNCTION_PARAMETER == "--binary":
        print("OS NAME : " + os.name)
        if not os.path.exists("./dist/market-connector" + get_binary_extension()):
            print("[ERROR] Binary file does not exist. Ending script.")
            exit(1)
        result = zip("./dist", DISTRO_DIRECTORY, APPLICATION_NAME + "-" + check_os_name(), APPLICATION_VERSION)
        if result is not None:
            # the version file should be created in the previous step of running with the --src flag
            print("[INFO] " + result + " is generated")
