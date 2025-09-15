from ghsync import main
from ghsync import sync

if __name__ == "__main__":
    config = main.config()

    cloned, failed_to_clone = sync.sync(
        config["backup_path"], config["username"], config["pat"]
    )
    updated, failed_to_update = sync.update(config["backup_path"])
