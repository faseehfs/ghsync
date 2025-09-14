from ghsync import main
from ghsync import sync

if __name__ == "__main__":
    config = main.config()

    cloned, failed = sync.sync(config["backup_path"], config["username"], config["pat"])
    print(f"Cloned: {cloned}\nFailed to clone: {failed}")

    updated, failed = sync.update(config["backup_path"])
    print(f"Updated: {updated}\nFailed to update: {failed}")
