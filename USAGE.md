# Usage

### Configuration

Before running the script, you must create environment variables with your F5XC Tenant URL and API Token.

```bash

export XC_API_TOKEN='XXXXXXXXX'
export XC_TENANT='f5-xctestdrive'

```

### Running the Script

To run the backup or restore functions, you will use the script files named `backup.py` and `restore.py`. These are the tools that perform the saving and applying of your network configurations.

### Example Outputs

The script will provide outputs that indicate the success or failure of the backup and restore operations. Unfortunately, due to a retrieval error, we cannot show the exact example outputs from the script. However, typically, a successful backup will indicate that the settings have been saved into a file, and a successful restore will confirm that the settings have been applied to the network.

### Permissions

It's important to note that in order to perform backups or restores, your API Key needs to have the right level of permission to access and change the network settings. This is like having the correct security clearance to make changes in a secure system[1].

### Conclusion

By following the above steps and ensuring you have the correct prerequisites, you can use the F5XC Backup/Restore Utilities to manage your network configurations effectively. Remember to consult the F5 documentation for detailed instructions on obtaining an API Token and for any additional support you may need.
