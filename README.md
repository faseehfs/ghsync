# GHSync

A simple, user-friendly Python CLI application for syncing your GitHub repositories to your local computer.

## Usage

1. Run `config`

    - Walks you through the configuration process.
    - Saves settings to `config.json`.
    - To edit later, either update `config.json` manually or re-run `config` to reset everything.

2. Run `sync`
    - Clones all repositories into your configured folder.
    - Handles LFS files if configured.
    - On subsequent runs:
        - Downloads new repositories.
        - Updates existing repositories.

## Extra Commands

-   `backup`  
    Compresses your backup directory into a timestamped `.zip` file and deletes the original folder. Next time you run `sync`, repositories are re-downloaded.
