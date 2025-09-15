import subprocess
import os
from . import utils


def sync(backup_dir, username, pat):
    repos = utils.get_all_github_repos(pat)

    if os.path.exists(backup_dir) and os.path.isdir(backup_dir):
        cloned_repos = os.listdir(backup_dir)
    else:
        cloned_repos = []

    repos_to_clone = []
    for repo in repos:
        if repo not in cloned_repos:
            repos_to_clone.append(repo)

    repos_cloned = []
    repos_failed_to_clone = []

    if len(repos_to_clone) > 1:
        print(f"Found {len(repos_to_clone)} new repositories: ")
        for repo in repos_to_clone:
            print(f"    {repo}")
    elif len(repos_to_clone) == 1:
        print(f"Found 1 new repository: {repos_to_clone[0]}")
    else:
        print("No new repositories has been found.")
        return repos_cloned, repos_failed_to_clone

    if repos_to_clone:
        for i, repo in enumerate(repos_to_clone):
            try:
                print("\r\033[K", end="")
                print(f"Downloading repo {i + 1}/{len(repos_to_clone)}: {repo}", end="")
                subprocess.run(
                    [
                        "git",
                        "clone",
                        "--mirror",
                        f"https://{username}:{pat}@github.com/{username}/{repo}.git",
                        f"{backup_dir}/{repo}/.git",
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except:
                repos_failed_to_clone.append(repo)
            else:
                repos_cloned.append(repo)
        print()

    return repos_cloned, repos_failed_to_clone
