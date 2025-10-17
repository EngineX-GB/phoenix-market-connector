"""
Name:           job_package.py
Description:    To package the versioned release of the core component
Date:           2022-11-27

Usage:

args:
    appDirectory    [required]      the directory of the app (to be packaged) that contains the app.json file

python job_package.py <appDirectory_containing_the_app.json_file>

e.g.

python job_package.py .././src

"""

import os
import datetime
import shutil
import sys
import job_versioning as jobVersion

CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
# Note: If you want this script to be used for other apps, then the CODE_DIRECTORY and APPLICATION_CONFIG will need to be generic.
# Also implies that the app's directory must have an app.json file in it.
CODE_DIRECTORY = sys.argv[1]
DISTRO_DIRECTORY = "./distro"
APPLICATION_CONFIG = jobVersion.readConfig(CODE_DIRECTORY)
APPLICATION_NAME = APPLICATION_CONFIG["application"]
APPLICATION_VERSION = APPLICATION_CONFIG["version"]

def zip(directoryPath, destinationPath):
    return shutil.make_archive(destinationPath + "/" + APPLICATION_NAME + "_" + APPLICATION_VERSION, "zip", directoryPath)


if (__name__=="__main__"):
    if not os.path.exists(DISTRO_DIRECTORY):
        print("[ERROR] " + DISTRO_DIRECTORY + " does not exist")
        sys.exit(1)
    if not os.path.exists(CODE_DIRECTORY):
        print("[ERROR] " + CODE_DIRECTORY + " does not exist")
        sys.exit(1)

    result = zip(CODE_DIRECTORY, DISTRO_DIRECTORY)
    if result is not None:
        print("[INFO] " + result + " is generated")