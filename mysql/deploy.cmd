::docker run -d --name timescaledb -p 5432:5432 --restart unless-stopped --network=mlplatform -e POSTGRES_PASSWORD=postgres timescale/timescaledb:latest-pg13
::postgresql://postgres:postgres@host.docker.internal:5432/postgres

::TODO: la seguente istruzione su windows causa problemi di permessi sulla cartella, da verificare
::docker run -d --name timescaledb -v C//mydata/timescaledb/data:/var/lib/postgresql/data -p 5432:5432 --restart unless-stopped --network=mlplatform -e POSTGRES_PASSWORD=postgres timescale/timescaledb:latest-pg13

docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql
::mysql+mysqlconnector://root:root@host.docker.internal:3306/mydb