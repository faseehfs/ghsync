from ghsync import main
from ghsync import sync

if __name__ == "__main__":
    config = main.config()

    cloned, failed_to_clone = sync.sync(
        config["backup_path"], config["username"], config["pat"]
    )
    updated, failed_to_update = sync.update(config["backup_path"])

    if not failed_to_clone and not failed_to_update:
        print("Syncing completed successfully.")
    else:
        print("Syncing completed with errors:")
        if failed_to_clone:
            print(f"ERROR: failed to clone {', '.join(failed_to_clone)}.")
        if failed_to_update:
            print(f"ERROR: failed to update {', '.join(failed_to_update)}.")
