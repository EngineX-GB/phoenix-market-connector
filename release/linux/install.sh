#!/bin/bash

# Market Connector installation for Linux (18/10/25)
# Suitable for a first time installation on linux.

# usage:

# Perform a fresh install of the connector
# sh install.sh --fresh
#
#
# Perform an update on an existing installation
# sh install.sh --update <existing_installation_of_phoenix_directory> <new_version>
# sh install.sh --update /c/users/dell/phoenix-v3 3.0.2
#
# Sets up the latest python version and installs the dependencies.
# sh install.sh --env-setup

CURRENT_LOCATION=$(pwd)
PHOENIX_HOME="${CURRENT_LOCATION}/phoenix-v3"
VERSION="3.0.2"

if [ $1 = "--env-setup" ]; then
  echo "[INFO] Setting up python and dependencies...."
  apt-get install -y python
  pip install beautifulsoup4==4.12.3 --no-input
  pip install requests==2.31.0 --no-input
  pip install cloudscraper==1.2.71 --no-input
  echo "Completed. Exiting."
  exit
fi

if [ $1 = "--update" ]; then
  PHOENIX_HOME= $2
  VERSION = $3
  echo "[INFO] Running update to version ${VERSION}."
  echo "[INFO]"
  echo "[INFO] Phoenix Directory : ${PHOENIX_HOME}"
  echo "[INFO]"

  # perform some checks before doing the update
  if [ ! -d "${PHOENIX_HOME}/src" ]; then
     echo "[ERROR] Directory ${PHOENIX_HOME} does not exist. Cannot proceed with update."
     exit
  fi
  rm -fr ${PHOENIX_HOME}/src
else
  # do this ONLY if it's a fresh install (i.e. not an update)
  echo "[INFO] As this is a a fresh install, remove any old instances of the connector"
  rm -fr "${PHOENIX_HOME}"
fi

INSTALL_DIR="${PHOENIX_HOME}/src"
TEMP_DIR="${PHOENIX_HOME}/install-temp"
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR"
# download file
curl -L -o ${TEMP_DIR}/phoenix.zip https://github.com/EngineX-GB/phoenix-market-connector/releases/download/${VERSION}/phoenix-mobile-connector_${VERSION}.zip
# unzip
if [ $? -eq 0 ]; then
    unzip "${TEMP_DIR}/phoenix.zip" -d "${INSTALL_DIR}"

    if [ -d "${PHOENIX_HOME}/properties" ]; then
      echo "[INFO] config.properties folder exists."
    else
      echo "[WARN] No existing config.properties file exists. Ensure one is created before using the connector."
    fi

    # perform clean up and remove temp folder
    echo "[INFO] Removing temporary files."
    rm -fr "${TEMP_DIR}"

else
    echo "[ERROR] Download failed. Skipping unzip."
fi
echo "[INFO] Installation complete."
