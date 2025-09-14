import click
import os
import json

CONFIG_FILE = "config.json"


def config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            configuration = json.load(f)
    else:
        configuration = {
            "username": input("Enter your GitHub username: "),
            "pat": input("Enter your PAT: "),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(configuration)
