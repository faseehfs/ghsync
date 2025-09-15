import requests
import subprocess
import os


def get_all_github_repos(pat):
    """
    Get all public and private repository names of a GitHub user using a Personal Access Token (PAT).

    :param username: GitHub username
    :param pat: Personal Access Token with 'repo' scope
    :return: List of repository names
    """
    repos = []
    url = f"https://api.github.com/user/repos"
    headers = {"Authorization": f"token {pat}"}
    params = {
        "visibility": "all",
        "affiliation": "owner",  # repos the user owns
        "per_page": 100,  # max per page
        "page": 1,
    }

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        data = response.json()
        if not data:
            break

        repos.extend([repo["name"] for repo in data])
        params["page"] += 1

    return repos


def sync(backup_dir, username, pat):
    repos = get_all_github_repos(pat)

    if os.path.exists(backup_dir) and os.path.isdir(backup_dir):
        cloned_repos = os.listdir(backup_dir)
    else:
        cloned_repos = []

    repos_to_clone = []
    for repo in repos:
        if repo not in cloned_repos:
            repos_to_clone.append(repo)

    print(f"New repositories found ({len(repos_to_clone)}): {repos_to_clone}")

    repos_cloned = []
    repos_failed_to_clone = []

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
                print(f"\nFailed to clone '{repo}'.")
                repos_failed_to_clone.append(repo)
            else:
                repos_cloned.append(repo)
        print()

    return repos_cloned, repos_failed_to_clone


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
            print(f"\nFailed to update '{repo}'.")
            failed_to_update.append(repo)
        else:
            updated.append(repo)

    print()
    return updated, failed_to_update
