# Usage

### Configuration

Before running the script, you must create environment variables with your F5XC Tenant URL and API Token.

```bash

export XC_API_TOKEN='XXXXXXXXX'
export XC_TENANT='f5-xctestdrive'

```

> [!NOTE]
> It's important to note that in order to perform backups or restores, your API Key needs to have the right level of permission to access and change the configuration settings.

### Running the Script

Command line options for the scripts can be found as follows:

```bash

backup-server$python3 /f5xc-backup-restore.py -h
usage: f5xc-backup-restore.py [-h] --action ACTION --path PATH --namespace NAMESPACE [--version]

F5XC Backup/Restore Utility Usage

options:
  -h, --help            show this help message and exit
  --action ACTION, -a ACTION
                        Desire Action - backup / restore
  --path PATH, -p PATH  Path to create backups in / restore backups from
  --namespace NAMESPACE, -n NAMESPACE
                        Namespace - comma deliminated
  --version             show program's version number and exit
```
