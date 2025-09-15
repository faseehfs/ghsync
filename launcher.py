import click
import sys

from ghsync import config
from ghsync import sync
from ghsync import backup


@click.group()
def cli():
    pass


@cli.command("config")
def configure():
    config.configure()


@cli.command("sync")
def synchronize():
    configuration = config.get()
    sync.sync(
        configuration["backup_path"], configuration["username"], configuration["pat"]
    )


@cli.command(name="backup")
def backup_dir():
    backup.backup(config.get()["backup_path"])


if __name__ == "__main__":
    cli()
