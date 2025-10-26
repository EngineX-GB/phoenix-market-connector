"""
Name:           job_versioning.py
Description:    To version the release of the core component
Date:           2022-11-27

Usage:

--appDirectory       [required]     the directory of the app that contains the app.json file
--updateMinorVersion [optional]     the minor version to be incremented
--updateMajorVersion [optional]     the major version to be incremented
--updatePatchVersion [optional]     the patch version to be incremented
--changeEntry        [optional]     a comment on this version (i.e. what changes are in the version to be stamped)

python job_versioning.py --appDirectory <directory_path_of_app_containing_app.json> --updateMinorVersion <minorversion> --updateMajorVersion <majorVersion> --updatePatchVersion <patchVersion> --changeEntry <comment>

python job_versioning.py --appDirectory .././src [ the default, which will only update the patch version]
python job_versioning.py --appDirectory .././src --updateMajorVersion
python job_versioning.py --appDirectory .././src --updateMinorVersion
python job_versioning.py --appDirectory .././src --updateMajorVersion --updateMinorVersion
python job_versioning.py --appDirectory .././src --updateMajorVersion --updateMinorVersion --changeEntry "This version has x change"
python job_versioning.py --appDirectory .././src --changeEntry "This version has x change"




"""

import os
import json
import datetime
import sys

PERIOD = "."
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

def readConfig(appDirectory):
    appConfigFile = open(appDirectory + "/app.json")
    appConfig = json.load(appConfigFile)
    appConfigFile.close()
    return appConfig

def updateConfig(appConfig, checkUpdateMajorVersion, checkUpdateMinorVersion):
    if appConfig["version"] is not None:
        version = appConfig["version"].split(".")
        majorVersion = int(version[0])
        minorVersion = int(version[1])
        patchVersion = int(version[2])
        if checkUpdateMajorVersion:
            majorVersion = majorVersion + 1
            minorVersion = 0
            patchVersion = 0
        elif checkUpdateMinorVersion:
            minorVersion = minorVersion + 1
            patchVersion = 0
        else: 
            patchVersion = patchVersion + 1
        newVersion = str(majorVersion) + PERIOD + str(minorVersion) + PERIOD + str(patchVersion)
        appConfig["version"] = newVersion
        appConfig["date"] = CURRENT_DATE
        return appConfig
    else:
        return None


def updateConfigWithChangeEntry(appConfig, entry):
    if appConfig is not None:
        appConfig["changeset"].append(CURRENT_DATE + " | " + entry)
    return appConfig


def save(appConfig, appDirectory):
    newAppConfig = json.dumps(appConfig,indent=4)
    f = open(appDirectory + "/app.json", "w", encoding="utf-8")
    f.write(newAppConfig)
    f.close()


if (__name__ == "__main__"):

    changeEntry = None
    appDirectory = None
    argCounter = 0

    for arg in sys.argv:    
        if arg == "--changeEntry":  
            changeEntry = sys.argv[argCounter + 1]
        if arg == "--appDirectory":
            appDirectory = sys.argv[argCounter + 1]

        argCounter = argCounter + 1  

    if appDirectory is None:
        print("[ERROR] AppDirectory is None")
        sys.exit(1)

    # needs to be changed if you want to reuse this versioning job for other apps
    appConfig = readConfig(appDirectory)
    checkUpdateMajorVersion = False
    checkUpdateMinorVersion = False

    if "--updateMajorVersion" in sys.argv:
        checkUpdateMajorVersion = True    
    if "--updateMinorVersion"  in sys.argv:
        checkUpdateMinorVersion = True

    updateConfig(appConfig, checkUpdateMajorVersion, checkUpdateMinorVersion)

    if changeEntry is not None:
        updateConfigWithChangeEntry(appConfig, changeEntry)
    
    save(appConfig, appDirectory)