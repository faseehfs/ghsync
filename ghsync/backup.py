import click
import shutil
from datetime import datetime


def backup(dir):
    """
    Converts the directory into a zip file in the same parent directory with a timestamp and deletes the original directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.make_archive(dir + "-" + timestamp, "zip", dir)
    shutil.rmtree(dir)
