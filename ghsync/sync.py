import click
import subprocess
import os
from . import utils


def download_new_repos(backup_dir, username, pat=""):
    """
    Downloads the repositories that have not been downloaded yet.
    """

    if pat:
        repos = utils.get_all_github_repos(pat)
    else:
        click.echo(
            click.style(
                "WARNING: PAT was not found. So, only your public repos will be synced.",
                fg="yellow",
            )
        )
        repos = utils.get_public_github_repos(username)

    cloned_repos = os.listdir(backup_dir) if os.path.isdir(backup_dir) else []
    repos_to_clone = [repo for repo in repos if repo not in cloned_repos]

    repos_cloned, repos_failed_to_clone = [], []

    if repos_to_clone:
        for repo in sorted(repos_to_clone):
            try:
                subprocess.run(
                    [
                        "git",
                        "clone",
                        "--mirror",
                        f"https://{username}:{pat}@github.com/{username}/{repo}.git",
                        f"{backup_dir}/{repo}",
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError:
                click.echo(click.style(f"Failed to clone {repo}.", fg="red"))
                repos_failed_to_clone.append(repo)
            else:
                click.echo(click.style(f"Cloned {repo}.", fg="green"))
                repos_cloned.append(repo)

    return len(repos_cloned), len(repos_to_clone)


def update_existing_repos(backup_dir, lfs=False):
    updated = []
    failed_to_update = []
    to_update = sorted(os.listdir(backup_dir))

    for i, repo in enumerate(to_update):
        repo_path = os.path.join(backup_dir, repo)

        try:
            subprocess.run(["git", "fetch", "--verbose"], cwd=repo_path, check=True)

            if lfs and utils.git_lfs_installed():
                subprocess.run(
                    ["git", "lfs", "fetch", "--all", "--verbose"],
                    cwd=repo_path,
                    check=True,
                )
            elif lfs:
                click.echo(
                    click.style(
                        f"ERROR: Unable to fetch LFS files because LFS was not installed.",
                        fg="red",
                    )
                )
        except subprocess.CalledProcessError:
            click.echo(click.style(f"Failed to update {repo}.", fg="red"))
            failed_to_update.append(repo)
        else:
            click.echo(click.style(f"Updated {repo}.", fg="green"))
            updated.append(repo)

    return len(updated), len(to_update)


def sync(backup_dir, username, pat, lfs=False):
    if not lfs:
        click.echo(
            click.style(
                "WARNING: LFS is not turned on. If you want to fetch LFS files, please turn it on from `config.json`.",
                fg="yellow",
            )
        )

    downloaded, to_download = download_new_repos(backup_dir, username, pat)
    updated, to_update = update_existing_repos(backup_dir, lfs)

    click.echo(
        f"\nDownloaded {downloaded}/{to_download}, updated {updated}/{to_update}.",
    )
