#!/bin/bash

# Market Connector installation for Linux (18/10/25)
# Suitable for a first time installation on linux and updates.

# usage:

# Perform a fresh install of the connector
# sh install.sh --fresh
#
#
# Perform an update on an existing installation
# sh install.sh --update <existing_installation_of_phoenix_directory> <new_version>
# sh install.sh --update /c/users/dell/phoenix-v3 3.0.14
#
# To install a local copy of the connector to the filesystem.
# sh install.sh --local-install <directory-path-of-zip>
# Note that the script must be local to the directory that you want to install the connector in.
#
#
# Perform an update on an existing installation assuming that the install.sh script is in the same level/
# directory level as the root Phoenix-v3 folder (that contains the src folder)
#
# sh install.sh --update <new_version>
# sh install.sh --update 3.0.2
#
# Sets up the latest python version and installs the dependencies.
# sh install.sh --env-setup

CURRENT_LOCATION=$(pwd)
PHOENIX_HOME="${CURRENT_LOCATION}/phoenix-v3"
VERSION="3.0.14"
IS_UPDATE="false"


# delete any temporary files from the previous run of this script
TEMP_DIR="install-temp"
rm -fr "${TEMP_DIR}"

# check that the required first argument is present before executing

if [ -z "$1" ]; then
  echo "[ERROR] First argument is required. Exiting."
  exit
fi

# check that valid arguments are set for installation
if [ "$1" = "--clean" ] || [ "$1" = "--update" ] || [ "$1" = "--help" ] || [ "$1" = "----env-setup" ]; then
  echo "[INFO] Preparing installation: $1"
else
  echo "[ERROR] First argument must be --clean, --update, --env-setup or --help"
  exit 1
fi

if [ $1 = "--help" ]; then
  echo "[INFO] Usage:"
  echo "[INFO] sh install.sh --clean <version_number>"
  echo "[INFO] sh install.sh --update <version_number>"
  echo "[INFO] sh install.sh --env-setup"
  echo "[INFO] sh install.sh --help"
  exit
fi

if [ $1 = "--env-setup" ]; then
  echo "[INFO] Setting up python and dependencies...."
  apt-get install -y python
  pip install beautifulsoup4==4.12.3 --no-input
  pip install requests==2.31.0 --no-input
  pip install cloudscraper==1.2.71 --no-input
  echo "[INFO] Completed. Exiting."
  exit
fi

if [ $1 = "--clean" ]; then
  if [ -z "$2" ]; then
    echo "[ERROR] Second argument (Version number) must be provided. Exiting."
    exit
  fi
  VERSION=$2
fi


if [ $1 = "--update" ]; then
  if [ -z "$2" ]; then
    echo "[ERROR] Second argument (Version number) must be provided. Exiting."
    exit
  fi

  VERSION=$2
  IS_UPDATE="true"
  echo "[INFO] Running update to version ${VERSION}."
  echo "[INFO]"
  echo "[INFO] Phoenix Directory : ${PHOENIX_HOME}"
  echo "[INFO]"
  # perform some checks before doing the update
  if [ ! -f "${PHOENIX_HOME}/market-connector" ]; then
     echo "[ERROR] Market connector in ${PHOENIX_HOME} does not exist. Cannot proceed with update."
     exit
  fi
  echo "[INFO] Attempting to delete ${PHOENIX_HOME}"
  rm -rf "${PHOENIX_HOME}"
fi


if [ "$IS_UPDATE" = "false" ]; then
  # do this ONLY if it's a fresh install (i.e. not an update)
  echo "[INFO] As this is a a fresh install, remove any old instances of the connector"
  rm -fr "${PHOENIX_HOME}"
fi

if [ $1 = "--local-install" ]; then
  echo "[INFO] Performing a local install of the connector"
  INSTALL_DIR="${PHOENIX_HOME}"
  TEMP_DIR="install-temp"
  mkdir -p "$INSTALL_DIR"
  mkdir -p "$TEMP_DIR"
  DISTRO_FILE_PATH=$2
  cp "$DISTRO_FILE_PATH" "$TEMP_DIR/phoenix.zip"
  unzip "${TEMP_DIR}/phoenix.zip" -d "${INSTALL_DIR}"
  if [ -d "${PHOENIX_HOME}/properties" ]; then
    echo "[INFO] Required configuration files exist. No further action required."
  else
    echo "[WARN] No existing config.properties file exists. Run application to automatically create one."
  fi

  # perform clean up and remove temp folder
  echo "[INFO] Removing temporary files."
  rm -fr "${TEMP_DIR}"
  exit
fi

INSTALL_DIR="${PHOENIX_HOME}"
TEMP_DIR="install-temp"
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR"
# download file
curl -L -o ${TEMP_DIR}/phoenix.zip https://github.com/EngineX-GB/phoenix-market-connector/releases/download/${VERSION}/phoenix-mobile-connector-linux_${VERSION}.zip
# unzip
if [ $? -eq 0 ]; then
    unzip "${TEMP_DIR}/phoenix.zip" -d "${INSTALL_DIR}"

    if [ -d "${PHOENIX_HOME}/../properties" ]; then
      echo "[INFO] Required configuration files exist. No further action required."
    else
      echo "[WARN] No existing config.properties file exists. Run application to automatically create one."
    fi

    # perform clean up and remove temp folder
    echo "[INFO] Removing temporary files."
    rm -fr "${TEMP_DIR}"

else
    echo "[ERROR] Download failed. Skipping unzip."
fi
echo "[INFO] Installation complete."
