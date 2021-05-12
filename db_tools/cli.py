import click
from datetime import datetime

from db_tools.config import Config
from db_tools.tools import (
    generate_duplicate_database,
    dump_database,
    restore_database,
)


@click.group()
def cli():
    pass


@click.command(name="dump")
@click.option("--config-file", "config_file", required=True)
@click.option("--backup-name", "backup_name", default="",
              help="text to be appended to the database name when generating a filename")
@click.option("--database", "database", default="",
              help="overrides the database name set in the config file")
def cli_dump_database(config_file, backup_name, database):
    """Dump database to a sql file. The path used is set by the "backup_path"
    variable in the config file.
    """

    config = Config(config_file)

    if backup_name == "":
        backup_name = datetime.now().strftime("%Y%m%d_%H%M")

    if database != "":
        config.database = database

    sql_file = config.backup_path.joinpath(f"{config.database}_{backup_name}.sql")
    dump_database(config, sql_file)


@click.command(name="restore")
@click.option("--config-file", "config_file", required=True)
@click.argument('path', required=True)
@click.argument('database', required=True)
def cli_restore_database(config_file, path, database):
    """Restore database from backup file. The name of the new database must be provided.
    """
    config = Config(config_file)
    restore_database(config, database, path)


@click.command(name="duplicate")
@click.option("--config-file", "config_file", required=True)
def cli_duplicate_database(config_file):
    """Generate a duplicate copy of a database with '_copy' appended to the name.
    """
    config = Config(config_file)
    generate_duplicate_database(config)


cli.add_command(cli_dump_database)
cli.add_command(cli_restore_database)
cli.add_command(cli_duplicate_database)
