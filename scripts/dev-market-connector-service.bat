@echo off
SET INGESTION_SERVICE_ENDPOINT=http://localhost:9000
SET CLIENT_SERVICE_ENDPOINT=http://localhost:9081
SET ENV=DEV
SET SERVICE_PORT=9001
SET SERVICE_HOST=127.0.0.1

%CD%\market-connector-service.exe

@echo on