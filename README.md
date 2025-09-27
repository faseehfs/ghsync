# GHSync

A simple, user-friendly Python CLI application for syncing your GitHub repositories to your local computer.

## Usage

### Step 1: Run `config`

This command walks you through the configuration process and saves the settings to `config.json` in the current directory. The available configurations are:

```json
{
    "username": "faseehfs", // mandatory
    "pat": "", // your GitHub Personal Access Token
    "backup_path": "backup", // relative or absolute path
    "lfs": false // fetch LFS files
}
```

### Step 2: Run `sync`

On the first run, this command downloads all your repositories to the `backup_path` specified in the config file. On subsequent runs, it checks for new repositories on GitHub and downloads them if not present locally, while updating existing ones.  
**Run this periodically to keep your local copy up to date.**

## Extra Commands

-   `backup`  
    Compresses your backup directory into a timestamped `.zip` file and deletes the original folder. The next time you run `sync`, repositories are re-downloaded. It is recommended to run this command occasionally to keep your repos safe.
