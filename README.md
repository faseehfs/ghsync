# GHSync

A simple, user-friendly Python CLI application for syncing your GitHub repositories to your local computer.

## Commands

-   `config`: Guides you through the configuration process and saves the settings to `config.json`. Run this again if you need to reconfigure the application.
-   `sync`: Downloads any repositories that haven’t been downloaded yet (including LFS files) and updates existing ones in the sync directory if there are changes. Run this periodically to keep your local copy up to date.
-   `backup`: Compresses your backup directory into a timestamped `.zip` file and deletes the original folder. The next time you run `sync`, repositories are re-downloaded, preventing local corruption.
