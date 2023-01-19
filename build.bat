cd scanner_api
docker build -t scanner-api:latest .

cd ..
cd scanner_db
docker build -t scanner-db:latest .