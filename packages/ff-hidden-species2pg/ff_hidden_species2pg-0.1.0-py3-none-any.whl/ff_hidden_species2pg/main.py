"""Default script file"""

import click

from .helpers import cli_message, create_table, insert_data


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    """Main CLI fct"""
    cli_message(f"Debug mode is {'on' if debug else 'off'}", "warning")


@cli.command("create-table")
@click.option("--conn-string", help="PostgreSQL connections string", required=True)
@click.option("--delete-table-if-exists", default=False, help="Delete table if exists")
def cli_create_table(conn_string: str, delete_table_if_exists):
    """Create PostgreSQL table src_lpodatas.t_c_..."""
    cli_message("Prepare to create table in database", "info")
    if delete_table_if_exists:
        cli_message(
            "CAUTION, table 'src_lpodatas.t_c_visionature_hidding_rules' will be deleted",
            "warning",
        )
    create_table(conn_string, delete_table_if_exists)


@cli.command("insert-data")
@click.option("--conn-string", help="PostgreSQL connections string", required=True)
@click.option("--flush-table", default=False, help="Flush all data in table")
def cli_insert_data(conn_string: str, flush_table: bool = False):
    """Populate rules in db"""
    cli_message("Prepare to download and insert data", "info")
    insert_data(conn_string, flush_table=flush_table)
