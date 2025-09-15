import click
import os
import json
import sys

CONFIG_FILE = "config.json"


def config():
    """
    Walks though the configuration process and stores the configuration in config.json which can be obtained later by calling config.get().
    """
    click.echo("Welcome. Let's configure the application. You only have to do it once!")

    configuration = {
        "username": input("Enter your GitHub username: "),
        "pat": input("Enter your PAT: "),
        "backup_path": input(
            "Enter the path to your backup folder (relative/absolute): "
        ),
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(configuration, f)
    click.echo("Configuration complete.")


def get():
    """
    Reads the config.json and returns it as a Python dictionary. Exits the application with exit code 1 if config.json is not found.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            configuration = json.load(f)
        return configuration
    else:
        click.echo(
            "Unable to locate config.json. Please run the `config` command to configure the application."
        )
        sys.exit(1)
