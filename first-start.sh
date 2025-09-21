docker compose down
rm -rf pgdata initdb skilldb/*
docker compose up skilldb -d
docker compose up postgres -d

sleep 10

docker exec -i postgres_container psql -U postgres -d keeperdb -f /dump.sql
docker exec -i skilldb psql -U postgres -d skilldb -f /dump.sql