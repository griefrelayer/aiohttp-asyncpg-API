#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  CREATE DATABASE $DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL
psql -v ON_ERROR_STOP=1 -d "$DB_NAME" -U "$DB_USER" <<-EOSQL
  CREATE TABLE IF NOT EXISTS employees (
    id          SERIAL          PRIMARY KEY,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR         NOT NULL,
    last_name   VARCHAR         NOT NULL,
    hire_date   DATE            NOT NULL
    );
EOSQL