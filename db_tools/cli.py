import click
from datetime import datetime
from pathlib import Path

from captif_db_config import Config

from db_tools import __version__
from db_tools.tools import (
    generate_duplicate_database,
    dump_database,
    restore_database,
)


@click.version_option(__version__, prog_name="db-tools")
@click.group()
def cli():
    pass


@click.command(name="dump")
@click.option("--config-file", "config_file", required=True)
@click.option("--backup-name", "backup_name", default="",
              help="text to be appended to the database name when generating a filename")
@click.argument("database", required=True)
@click.argument("tables", nargs=-1)
@click.argument("backup-path", required=True)
def cli_dump_database(config_file, backup_name, database, tables, backup_path):
    """Dump database to a sql file.
    """

    config = Config(config_file)

    if backup_name == "":
        backup_name = datetime.now().strftime("%Y%m%d_%H%M")

    sql_file = Path(backup_path).joinpath(f"{database}_{backup_name}.sql")
    dump_database(config, database, sql_file, tables)


@click.command(name="restore")
@click.option("--config-file", "config_file", required=True)
@click.argument('database', required=True)
@click.argument('path', required=True)
def cli_restore_database(config_file, database, path):
    """Restore database from backup file. The name of the new database must be provided.
    """
    config = Config(config_file)
    restore_database(config, database, path)


@click.command(name="duplicate")
@click.option("--config-file", "config_file", required=True)
@click.argument('database', required=True)
@click.argument("tables", nargs=-1)
def cli_duplicate_database(config_file, database, tables):
    """Generate a duplicate copy of a database with '_copy' appended to the name.
    """
    config = Config(config_file)
    generate_duplicate_database(config, database, tables)


cli.add_command(cli_dump_database)
cli.add_command(cli_restore_database)
cli.add_command(cli_duplicate_database)


if __name__ == '__main__':
    cli()
