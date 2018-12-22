#!/bin/bash
######################################################################
# Set up database for development
######################################################################

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOF
	CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
	CREATE DATABASE $DB_NAME OWNER=$DB_USER;
EOF

psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" < /schema.sql
