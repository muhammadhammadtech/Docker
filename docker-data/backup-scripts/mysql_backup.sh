#!/bin/bash
BACKUP_DIR="/backup/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "Creating MySQL backup..."
docker exec mysql-prod mysqldump \
  -u root -pSecureRootPass123! \
  --single-transaction --routines --triggers \
  production_db > "$BACKUP_DIR/mysql_backup_$TIMESTAMP.sql"

gzip "$BACKUP_DIR/mysql_backup_$TIMESTAMP.sql"

docker run --rm \
  --mount source=mysql_data,target=/data \
  -v $HOME/docker-backups:/backup \
  ubuntu:latest \
  tar czf "/backup/mysql_volume_$TIMESTAMP.tar.gz" -C /data .

echo "MySQL backup done: mysql_backup_$TIMESTAMP.sql.gz"
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete
