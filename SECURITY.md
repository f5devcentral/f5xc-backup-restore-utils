# Security

## Credentials

The script will use credentials from an API Token to authenticate with the F5 Distributed Cloud API. The API Token is stored in a file called `config.ini` in the `.f5xc` directory.

```bash
cd .f5xc
cat > config.ini<< EOF
[DEFAULT]
token=XXXXXXXX
tenant=f5xc-testdrive
EOF
```

The file should be readable only by the user running the script.

```bash
chmod 600 .f5xc/config.ini
```

## Permissions

The script should be run as a user with the minimum required permissions to perform the necessary operations. The user should have read and write permissions to the script, as well as read permissions to the backup directory.

```bash
chown -R f5xc-service-account:f5xc-operations-group /path/to/script-output
chmod -R 750 /path/to/script-output
```

If additional users need to run the script, they should be added to the `f5xc-operations-group` group.

```bash
usermod -a -G f5xc-operations-group additional-backup-user
```

## Reporting a Vulnerability

The contributors to this project take security seriously. If you believe
you have found a security vulnerability, please report it
to as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report any potential or current instances of security
vulnerabilities to [ss@f5.com](mailto:ss@f5.com)

For more information on reporting vulnerabilities with F5, visit
[https://www.f5.com/services/support/report-a-vulnerability](https://www.f5.com/services/support/report-a-vulnerability)
