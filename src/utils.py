import requests
import sys
import subprocess


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
            raise Exception(f"Failed to fetch repos: {response.status_code}")

        data = response.json()
        if not data:
            break

        repos.extend([repo["name"] for repo in data])
        params["page"] += 1

    return repos


def get_public_github_repos(username):
    """
    Fetch all public repository names for a given GitHub username.

    Args:
        username (str): GitHub username.

    Returns:
        list: List of repository names.
    """
    url = f"https://api.github.com/users/{username}/repos"
    repos = []
    page = 1

    while True:
        response = requests.get(url, params={"per_page": 100, "page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repos: {response.status_code}")

        data = response.json()
        if not data:
            break

        repos.extend(repo["name"] for repo in data)
        page += 1

    return repos


def git_lfs_installed():
    try:
        subprocess.run(
            ["git", "lfs", "version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
