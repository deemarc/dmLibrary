docker run -d \
    --name dmLibrary_db \
    -p 127.0.0.1:5442:5432 \
    -e POSTGRES_USER=dmLibrary_usr \
    -e POSTGRES_PASSWORD=dmLibrary_pass \
    -e POSTGRES_DB=dmLibrary_dev \
    postgres
