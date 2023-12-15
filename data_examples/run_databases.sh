#!/bin/sh

docker run -d --name postgres_db -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:latest

docker run -d --name mysql_db -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql:latest
