# core-db
_______________________________________________________________________________

This project/library contains common elements related to database engines and 
provides clients to simplify the connections...

## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```shell
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```shell
source .venv/bin/activate
```

### Install required libraries.
```shell
pip install .
```

### Optional libraries.
```shell
pip install '.[all]'  # For all...
pip install '.[mysql]'
pip install '.[postgre]'
pip install '.[oracle]'
pip install '.[mongo]'
pip install '.[mssql]'
pip install '.[snowflake]'
pip install '.[db2]'
```

### Check tests and coverage...
```shell
python manager.py run-tests
python manager.py run-coverage
```

## Clients

### Postgre
```python
from core_db.engines.postgre import PostgreClient

with PostgreClient(conninfo=f"postgresql://postgres:postgres@localhost:5432/test") as client:
    client.execute("SELECT version() AS version;")
    print(client.fetch_one()[0])
```

### Mongo
```python
from core_db.engines.mongo import MongoClient

client = MongoClient(**{"host": "host", "database": "db"})
client.connect()
print(client.test_connection())
```

### MsSql
```python
from core_db.engines.mssql import MsSqlClient

with MsSqlClient(
        dsn="DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=master;UID=SA;PWD=sOm3str0ngP@33w0rd;Encrypt=no",
        autocommit=True, timeout=5) as client:
    
    client.execute("SELECT @@VERSION AS 'version';")
    print(list(client.fetch_records()))
```

### Oracle
```python
from core_db.engines.oracle import OracleClient

with OracleClient(user="...", password="...", dsn=f"{host}:{port}/{service_name}") as client:
    res = client.execute("SELECT * FROM ...")
    for x in client.fetch_all():
        print(x)
```

### MySQL
```python
from core_db.engines.mysql import MySQLClient

with MySQLClient(host="localhost", user="root", password="SomePassword") as client:
    client.execute("SELECT * FROM ...;")
    for x in client.fetch_all():
        print(x)
```

### Snowflake
```python
...
```

### Testing clients...
We can test the clients by executing the below command. It will perform a series of
query execution in the database engine to ensure it's working as expected. We
must have the database engine up and running...

Example PostgreSQL:
```commandline
docker run --env=POSTGRES_PASSWORD=postgres --env=PGDATA=/var/lib/postgresql/data --volume=/var/lib/postgresql/data -p 5432:5432 -d postgres:12.18-bullseye
python manager.py run-database-test -db PostgreClient -params '{"conninfo":"postgresql://postgres:postgres@localhost:5432/postgres"}'
```

Example MySQL:
```shell
docker run --env=MYSQL_ROOT_PASSWORD=mysql_password --volume=/var/lib/mysql -p 3306:3306 --restart=no --runtime=runc -d mysql:latest
python manager.py run-database-test -db MySQLClient -params '{"host": "localhost", "database": "sys", "user": "root", "password": "mysql_password"}'
```

Example Oracle:
```shell
docker pull container-registry.oracle.com/database/express:latest
docker container create -it --name OracleSQL -p 1521:1521 -e ORACLE_PWD=oracle_password container-registry.oracle.com/database/express:latest
docker start OracleSQL
python manager.py run-database-test -db OracleClient -params '{"user": "system", "password": "oracle_password", "dsn": "localhost:1521/xe"}'
```
![How to connect](./assets/OracleCxn.png)

Example MsSQL:
```shell
docker pull mcr.microsoft.com/mssql/server:2022-latest

docker run\
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=sOm3str0ngP@33w0rd" \
  -p 1433:1433 --name MsSQL --hostname MsSQL \
  -d \
  mcr.microsoft.com/mssql/server:2022-latest

docker start MsSQL

sudo /bin/bash ./scripts/install_mssql_driver.sh
python manager.py run-database-test -db MsSqlClient -params '{"dsn": "DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=master;UID=SA;PWD=sOm3str0ngP@33w0rd;Encrypt=no"}'
```

Example DB2:
```shell
curl https://public.dhe.ibm.com/software/ibmi/products/odbc/debs/dists/1.1.0/ibmi-acs-1.1.0.list | sudo tee /etc/apt/sources.list.d/ibmi-acs-1.1.0.list
sudo apt update
sudo apt install ibm-iaccess
```
