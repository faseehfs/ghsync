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
    "username": "faseehfs",
    "pat": "",
    "backup_path": "backup",
    "lfs": false
}
```

-   `username`: Your GitHub username.
-   `pat`: Personal Access Token (optional, needed only if private repos require it).
-   `backup_path`: Folder for storing your repositories (default: `backup`).
-   `lfs`: Set to `true` if you want Git LFS files; default is `false`.

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
