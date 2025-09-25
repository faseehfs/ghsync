import click
import subprocess
import os
from . import utils


def download_repos(backup_dir, username, pat=""):
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
        click.echo(f"Found {len(repos_to_clone)} new repositories: ")
        for repo in repos_to_clone:
            click.echo(f"    {repo}")
    elif len(repos_to_clone) == 1:
        click.echo(f"Found 1 new repository: {repos_to_clone[0]}")
    else:
        click.echo("No new repository has been found.")
        return repos_cloned, repos_failed_to_clone

    if repos_to_clone:
        for i, repo in enumerate(repos_to_clone):
            try:
                click.echo("\r\033[K", nl=False)
                click.echo(
                    f"Downloading repos ({i + 1}/{len(repos_to_clone)}): {repo}",
                    nl=False,
                )
                subprocess.run(
                    [
                        "git",
                        "clone",
                        "--mirror",
                        f"https://{username}:{pat}@github.com/{username}/{repo}.git",
                        f"{backup_dir}/{repo}",
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                click.echo("CalledProcessError")
                repos_failed_to_clone.append(repo)
            else:
                repos_cloned.append(repo)
        click.echo()

    return repos_cloned, repos_failed_to_clone


def update(backup_dir, lfs=False):
    updated = []
    failed_to_update = []
    to_update = os.listdir(backup_dir)

    for i, repo in enumerate(to_update):
        repo_path = os.path.join(backup_dir, repo)

        try:
            click.echo("\r\033[K", nl=False)
            click.echo(f"Updating repos ({i + 1}/{len(to_update)}): {repo}", nl=False)

            subprocess.run(
                ["git", "fetch"],
                cwd=repo_path,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if lfs:
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

    click.echo()
    return updated, failed_to_update


def sync(backup_dir, username, pat, lfs=False):
    if not lfs:
        click.echo(
            click.style(
                "WARNING: LFS is not turned on. If you want to fetch LFS files, please turn it on from `config.json`.",
                fg="yellow",
            )
        )

    cloned, failed_to_clone = download_repos(backup_dir, username, pat)
    updated, failed_to_update = update(backup_dir, lfs)

    if any((failed_to_clone, failed_to_update)):
        click.echo("Syncing completed with errors:")
        error_messages = []
        if failed_to_clone:
            error_messages.append(
                f"ERROR: failed to clone {', '.join(failed_to_clone)}."
            )
        if failed_to_update:
            error_messages.append(
                f"ERROR: failed to update {', '.join(failed_to_update)}."
            )

        click.echo(click.style("\n".join(error_messages), fg="red"))
    else:
        click.echo("Syncing completed successfully.")
