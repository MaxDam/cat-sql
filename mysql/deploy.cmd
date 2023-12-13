:: POSTGRESQL
::docker run -d --name timescaledb -p 5432:5432 --restart unless-stopped --network=mlplatform -e POSTGRES_PASSWORD=postgres timescale/timescaledb:latest-pg13
::psql -U postgres -d mydb -f query.sql
::conn_str: postgresql://postgres:postgres@host.docker.internal:5432/postgres

:: MYSQL
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql
timeout /nobreak /t 10 > nul
docker exec -i mysql mysql -u root -p root mydb < create_db_mysql.sql

::conn_str: mysql+mysqlconnector://root:root@host.docker.internal:3306/mydb
