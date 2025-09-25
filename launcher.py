import click

from ghsync import config
from ghsync.sync import sync
from ghsync.backup import backup


@click.group()
def cli():
    pass


@cli.command("config")
def config_command():
    config.config()


@cli.command("sync")
def sync_command():
    sync(
        configuration["backup_path"],
        configuration["username"],
        configuration["pat"],
        configuration["lfs"],
    )


@cli.command(name="backup")
def backup_dir():
    backup(configuration["backup_path"])


if __name__ == "__main__":
    configuration = config.get()
    cli()
