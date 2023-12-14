#!/bin/sh

# POSTGRESQL
#docker run -d --name timescaledb -p 5432:5432 --restart unless-stopped --network=mlplatform -e POSTGRES_PASSWORD=postgres timescale/timescaledb:latest-pg13
#conn_str: postgresql://postgres:postgres@host.docker.internal:5432/postgres

# MYSQL
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql
#conn_str: mysql+mysqlconnector://root:root@host.docker.internal:3306/mydb
