#!/bin/bash

CURRENT_LOCATION=$(pwd)
PHOENIX_HOME="${CURRENT_LOCATION}/phoenix-v3"
rm -fr "${PHOENIX_HOME}"
INSTALL_DIR="${PHOENIX_HOME}/src"
TEMP_DIR="${PHOENIX_HOME}/install-temp"
mkdir -p "$INSTALL_DIR"
mkdir -p "$TEMP_DIR"
# download file
curl -L -o ${TEMP_DIR}/phoenix.zip https://github.com/EngineX-GB/phoenix-market-connector/releases/download/3.0.2/phoenix-mobile-connector_3.0.2.zip
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