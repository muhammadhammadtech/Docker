#!/bin/bash
BACKUP_DIR="/backup/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "Creating PostgreSQL backup..."
docker exec postgres-prod pg_dumpall -U postgres \
  > "$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"

gzip "$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"

docker run --rm \
  --mount source=postgres_data,target=/data \
  -v $HOME/docker-backups:/backup \
  ubuntu:latest \
  tar czf "/backup/postgres_volume_$TIMESTAMP.tar.gz" -C /data .

echo "PostgreSQL backup done: postgres_backup_$TIMESTAMP.sql.gz"
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete
