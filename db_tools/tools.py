"""
Database-specific tools.
The module includes functions for generating duplicate copies of a database (which can be
used for testing), as well as creating database ER diagrams to document the structure of
a database.
"""

from typing import List, Union
import subprocess
from pathlib import Path


"""
Database create, drop, duplicate, dump
"""


def mysql_base_command(url: str, port: int, username: str, password: str) -> List[str]:
    return ["mysql", "-u", username, f"-p{password}", "-h", url, "-P", str(port)]


def mysql_restore_command(
    url: str, port: int, username: str, password: str, database: str
) -> List[str]:
    """Generate a command to restore a database. The resulting command can be used by
    subprocess.call() with the stdin attribute.
    :param url: Database server host name.
    :param port: Database server port number.
    :param username: Database server username.
    :param password: Database server password.
    :param database: Name of the database to drop.
    """
    return mysql_base_command(url, port, username, password) + ["-A", f"-D{database}"]


def call_mysql_command(url: str, port: int, username: str, password: str, cmd: str):
    """Call mysql bash command.
    :param url: Database server host name.
    :param port: Database server port number.
    :param username: Database server username.
    :param password: Database server password.
    :param cmd: mysql command.
    """
    try:
        subprocess.run(
            mysql_base_command(url, port, username, password),
            input=bytes(cmd, encoding="ascii"),
        )
    except Exception as e:
        print(e.args)


def mysql_dump_command(
    url: str, port: int, username: str, password: str, database: str,
    tables: List[str] = [], exclude: List[str] = [],
) -> List[str]:
    """
    Generate a command to dump a database. The resulting command can be used by
    subprocess.call() with the stdout attribute set to a file object.
    :param url: Database server host name.
    :param port: Database server port number.
    :param username: Database server username.
    :param password: Database server password.
    :param database: Name of the database.
    :param tables: List of tables to use (optional). Defaults to all tables in the database.
    :param exclude: List of tables to ignore (optional).
    """
    return [
        "mysqldump",
        "-u",
        username,
        f"-p{password}",
        "-h",
        url,
        "-P",
        str(port),
        "--set-gtid-purged=OFF",
        "--triggers",
        "--routines",
        database,
        *tables,
        *[f"--ignore-table={database}.{tt}" for tt in exclude]
    ]


def dump_database(config, database, path: Union[str, Path], tables: List[str] = []):
    """Dumps the database to a file.
    :param database: Name of the database to dumped.
    :param path: File path used store the dumped database.
    :param tables: List of tables to use (optional). Defaults to all tables in the database.
    """
    with open(path, "w") as f:
        subprocess.call(
            mysql_dump_command(
                config.HOST,
                config.PORT,
                config.USERNAME,
                config.PASSWORD,
                database,
                tables,
            ), stdout=f
        )


def drop_database(url: str, port: int, username: str, password: str, database: str):
    """Drop database. Only available for 'test' and 'copy' databases.
    :param url: Database server host name.
    :param port: Database server port number.
    :param username: Database server username.
    :param password: Database server password.
    :param database: Name of the database to drop.
    """
    if ("test" not in database) and ("copy" not in database):
        print("'drop_databases' is only available for 'test' and 'copy' databases.")
        print("Production databases can only be dropped manually.")
        return None
    call_mysql_command(url, port, username, password, f"DROP DATABASE {database};")


def create_database(url: str, port: int, username: str, password: str, database: str):
    """Create an empty database.
    :param url: Database server host name.
    :param port: Database server port number.
    :param username: Database server username.
    :param password: Database server password.
    :param database: Name of the new database.
    """
    call_mysql_command(url, port, username, password, f"CREATE DATABASE {database};")


def restore_database(config, database: str, sql_file: Union[str, Path]):
    """Restore database from sql file.
    :param database: Name of the database to restore
    :param sql_file: Path to back-up sql file
    """
    db_params = (
        config.HOST,
        config.PORT,
        config.USERNAME,
        config.PASSWORD,
    )

    create_database(*db_params, database)

    with open(sql_file, "r") as f:
        subprocess.call(mysql_restore_command(*db_params, database), stdin=f)


def generate_duplicate_database(
    config, database, tables: List[str] = [], exclude: List[str] = [],
):
    """Generates a duplicate database with '_copy' appended to the database name. The
    duplicate database can be used to test alembic migrations before they are applied to
    the production database. Connection credentials are read from the config file.
    :param database: Name of the database to duplicate.
    :param tables: List of tables to use (optional). Defaults to all tables in the database.
    :param exclude: List of tables to ignore (optional).
    """
    db_params = (
        config.HOST,
        config.PORT,
        config.USERNAME,
        config.PASSWORD,
    )

    ps = subprocess.Popen(
        mysql_dump_command(*db_params, database, tables, exclude), stdout=subprocess.PIPE,
    )

    duplicate_database = f"{database}_copy"
    drop_database(*db_params, duplicate_database)
    create_database(*db_params, duplicate_database)

    subprocess.call(
        mysql_restore_command(*db_params, duplicate_database), stdin=ps.stdout,
    )
