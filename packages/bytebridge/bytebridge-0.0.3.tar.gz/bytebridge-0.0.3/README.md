

<p align="center" style="padding: 20px">
  <img src="static/branding/logo.svg" style="width:450px" alt="bytebridge">
</p>

<p align="center">
    <em>A data tool designed to move data seamlessly between various sources and destinations.</em>
</p>

<p align="center">
    <a href="https://pypi.org/project/bytebridge" target="_blank">
        <img src="https://img.shields.io/pypi/v/bytebridge?" alt="Package version">
    </a>
</p>


## CLI

Bytebridge aims to have a CLI that can be used to easily transfer data from multiple sources. Some examples are shown below:

### Parquet to PostgreSQL

```bash
bytebridge transfer \
    --connections connections.json \
    --source parquet_conn \
    --source-object data.parquet \
    --target postgresql_conn \
    --target-object bytebridge.public.data
```
### PostgreSQL to Parquet

```bash
bytebridge transfer \
    --connections connections.json \
    --source postgresql_conn \
    --source-object bytebridge.public.data \
    --target postgresql_conn \
    --target-object data.parquet
```

In both cases, the connections metadata are defined in the `connections.json` file. An example of the file definition is:

```json
{
    "parquet_conn": {
        "type": "parquet"
    },
    "postgresql_conn": {
        "type": "postgresql",
        "parameters": {
            "host": "[hostname_of_the_connection]",
            "user": "[postgresql_username_to_be_used]",
            "password": "[postgresql_password_to_be_used]",
            "port": "[postgresql_port_to_be_used]",
        }
    }
}
```


## API

Coming soon.

## Data Connectors

### Currently Supported

| Name             | Type          | Client                                                                         |
|----------------- | --------------|--------------------------------------------------------------------------------|
| PostgreSQL       | Database      | [psycopg](https://pypi.org/project/psycopg/)                                   |
| MySQL            | Database      | [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)     |
| MS SQL Server    | Database      | [pymssql](https://pypi.org/project/pymssql/)                                   |
| Parquet          | File          | [pyarrow](https://pypi.org/project/pyarrow/)                                   |
| CSV              | File          | [csv](https://docs.python.org/3/library/csv.html)                              |



### Planned

| Name             | Type          |
|----------------- | --------------|
| SQLite           | Database      |
| MongoDB          | Database      |
| MariaDB          | Database      |
| Clickhouse       | Database      |
| BigQuery         | Database      |
| Oracle           | Database      |
| Cassandra        | Database      |
| ORC              | File          |
| Avro             | File          |
| Excel (XLSX)     | File          |
| JSON             | File          |



## Contributing

Feel free to contribute to this project. See the contribution guidelines in [here](CONTRIBUTING.md).

## License

This project is licensed under the terms of the [Apache 2.0 license](LICENSE).