# GHSync

A straightforward Python CLI tool to sync your GitHub repositories to your local machine.

## Usage

### 1. Configure

Run:

```bash
ghsync config
```

This guides you through setup and saves your settings in `config.json` in the current directory:

```json
{
    "username": "",
    "pat": "",
    "backup_path": "",
    "lfs": true,
    "ignored_repos": ["repo-1", "repo-2"]
}
```

-   `username`: Your GitHub username.
-   `pat`: Personal Access Token (optional; required only for syncing private repos).
-   `backup_path`: Folder where your repositories will be stored (default: `backup`).
-   `lfs`: Set to `true` to include Git LFS files; default is `false`.
-   `ignored_repos`: List the names of repos to ignore, or leave empty to sync all.

### 2. Sync Repositories

Run:

```bash
ghsync sync
```

-   First run: Downloads all your repositories to `backup_path`.
-   Subsequent runs: Updates existing repos and fetches any new ones.

**Tip:** Run periodically to keep your local copy current.

## Additional Commands

-   `backup`  
    Compresses your backup folder into a timestamped `.zip` and deletes the original. Next time you run `sync`, repos are re-downloaded. Useful for safe storage.
