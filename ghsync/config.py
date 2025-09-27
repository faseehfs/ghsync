import click
import os
import json
import sys

from getpass import getpass

CONFIG_FILE = "config.json"


def config():
    click.echo("Welcome. Let's configure the application. You only have to do it once!")

    configuration = {
        "username": input("Enter your GitHub username: "),
        "pat": getpass("Enter your PAT (press Enter to skip this step): "),
        "backup_path": input(
            "Enter the relative/absolute path to your backup folder (press Enter to use the default): "
        ),
        "lfs": input(
            "Do you want to fetch LFS files when you sync? If you are unsure, press Enter. (y/N): "
        )
        .strip()
        .lower()
        == "y",
    }

    if configuration["backup_path"] == "" or configuration["backup_path"].isspace():
        configuration["backup_path"] = "backup"

    with open(CONFIG_FILE, "w") as f:
        json.dump(configuration, f, indent=4)
    click.echo("Configuration complete.")


def get():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            configuration = json.load(f)
        return configuration
    else:
        return None
