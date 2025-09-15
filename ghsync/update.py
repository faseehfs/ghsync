import subprocess
import os


def update(backup_dir):
    updated = []
    failed_to_update = []
    to_update = os.listdir(backup_dir)

    for i, repo in enumerate(to_update):
        repo_path = os.path.join(backup_dir, repo)

        try:
            print("\r\033[K", end="")
            print(f"Updating repo {i + 1}/{len(to_update)}: {repo}", end="")

            subprocess.run(
                ["git", "fetch"],
                cwd=repo_path,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "lfs", "fetch", "--all"],
                cwd=repo_path,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except:
            failed_to_update.append(repo)
        else:
            updated.append(repo)

    print()
    return updated, failed_to_update
