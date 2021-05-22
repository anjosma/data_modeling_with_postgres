## How run the project
Pull the Postgres Docker Image:
```console
$ docker pull postgres
```
Create a container called `db_postgres_student` given the Postgres user, password and database name as environment variables:
```console
$ docker run --name db_postgres_student -e POSTGRES_USER=student -e POSTGRES_PASSWORD=student -e POSTGRES_DB=studentdb -p 5432:5432 -d postgres
```
