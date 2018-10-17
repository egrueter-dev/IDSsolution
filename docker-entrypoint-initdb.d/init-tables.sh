#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username dbusr --dbname web <<-EOSQL
        CREATE TABLE  weblogs (
               day    date,
               status varchar(3)
               );
EOSQL
