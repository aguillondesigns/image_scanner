#!/bin/sh

cd scanner_api/
docker build -t scanner-api:latest .

cd ../scanner_db/
docker build -t scanner-db:latest .

cd ../