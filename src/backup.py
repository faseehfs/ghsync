import click
import shutil
import os
from datetime import datetime


def backup(dir):
    """
    Converts the directory into a zip file in the same parent directory with a timestamp and deletes the original directory.
    """
    if not os.path.exists(dir):
        click.echo(f"'{dir}' doesn't exist.")
        return
    if not os.path.isdir(dir):
        click.echo(f"'{dir}' is not a directory.")
        return

    timestamp = datetime.now().strftime("-%Y-%m-%d_%H-%M-%S")
    shutil.make_archive(dir + timestamp, "zip", dir)
    shutil.rmtree(dir)
    click.echo("Backup has been created successfully.")
