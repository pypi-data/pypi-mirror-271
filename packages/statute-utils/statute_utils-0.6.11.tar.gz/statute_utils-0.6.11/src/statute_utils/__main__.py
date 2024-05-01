from pathlib import Path

import click

from .config import setup_local_statute_db


@click.group()
def cli():
    """Wrapper of commands for statute-utils."""
    pass


@cli.command()
@click.option(
    "--folder",
    default="../corpus-statutes",
    required=True,
    help="Location of raw files to create database",
)
def init_db(folder: str):
    setup_local_statute_db(Path(folder))


if __name__ == "__main__":
    cli()
