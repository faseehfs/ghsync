import click
import os
import json
import requests

CONFIG_FILE = "config.json"


def config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            configuration = json.load(f)
    else:
        print(
            "Welcome. Let's configure the application. You only have to do it once!\n"
        )

        configuration = {
            "username": input("Enter your GitHub username: "),
            "pat": input("Enter your PAT: "),
            "backup_path": input(
                "Enter the path to your backup folder (relative/absolute): "
            ),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(configuration, f)
    return configuration
