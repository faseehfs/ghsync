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
    logs = []
    repos = get_all_github_repos(pat)

    if os.path.exists(backup_dir) and os.path.isdir(backup_dir):
        cloned_repos = os.listdir(backup_dir)
    else:
        cloned_repos = []

    repos_cloned = []
    repos_failed_to_clone = []

    for repo in repos:
        if repo in cloned_repos:
            continue

        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    f"https://{username}:{pat}@github.com/{username}/{repo}.git",
                    f"{backup_dir}/{repo}/.git",
                ],
                check=True,
            )
        except:
            repos_failed_to_clone.append(repo)
        else:
            repos_cloned.append(repo)

    return repos_cloned, repos_failed_to_clone
