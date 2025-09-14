import requests
import subprocess
import os


def get_all_github_repos(username, pat):
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


def sync(username, pat):
    backup_dir = "backup"
    repos = get_all_github_repos(username, pat)
    cloned_repos = os.listdir(backup_dir)

    for repo in repos:
        if repo in cloned_repos:
            continue

        subprocess.run(
            "git",
            "clone",
            f"https://{username}:{pat}@github.com/{username}/{repo}.git",
            "backup",
        )
