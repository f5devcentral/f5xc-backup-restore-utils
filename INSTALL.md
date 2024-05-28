# Installation Instructions

## Prerequisites

Before you begin, ensure that you have:

- A Linux-based system (such as Red Hat Enterprise Linux or CentOS)
- Administrative privileges on the system
- Internet access to download necessary files

[Running the script via a service account](#creating-a-service-account)

## Installation Steps

> [!NOTE]
> The steps below are shown are applicable for Red Hat Enterprise Linux or CentOS

1. **Install Python 3.x**
   The script requires Python 3.x to run. You can install Python 3 using the following command:

   ```bash
   sudo yum install python3
   ```

2. **Install Git**
   Git is used to clone the repository from GitHub. Install Git with the following command:

   ```bash
   sudo yum install git
   ```

3. **Clone the Repository**
   Use Git to clone the `f5xc-backup-restore-utils` repository to your local system:

   ```bash
   git clone https://github.com/f5devcentral/f5xc-backup-restore-utils.git
   ```

4. **Navigate to the Script Directory**
   Change into the directory where the script is located:

   ```bash
   cd f5xc-backup-restore-utils
   ```

5. **Set Execution Permissions**
   Make the script executable with the following command:

   ```bash
   chmod +x f5xc-backup-restore.py
   ```

6. **Checking credentials**
   Before running the script, you need to configure it with your F5XC Tenant URL and API Token. Refer to [the following to create a config.ini file with your credentials](./SECURITY.md#credentials)

7. **Run the Script**
   You can now run the backup or restore script using the following commands:

   ```bash
   ./f5xc-backup-restore.py
   ```

## Creating a Service Account

1. **Create a New User**
   Create a new user account on the Linux system with the following command:

   ```bash
   sudo useradd -m f5xc-service-account
   ```

2. **Set a Password**
   Set a password for the new user account:

   ```bash
   sudo passwd f5xc-service-account
   ```

3. **Create a New Group**
   Create a new group for the service account:

   ```bash
   sudo groupadd f5xc-operations-group
   ```

4. **Add the User to the Group**
   Add the user to the group:

   ```bash
   sudo usermod -a -G f5xc-operations-group f5xc-service-account
   ```

5. **Installing script to an accessible location**
   Copy the script to a location accessible by the service account:

   ```bash
   sudo cp f5xc-backup-restore.py /usr/local/bin
   ```

6. **Set Permissions**
   Set the permissions on the script to allow execution from a service account and its group:

   ```bash
   sudo chmod 750 /usr/local/bin/f5xc-backup-restore.py
   ```

7. **Set Ownership**
   Set the ownership of the script to the service account and group:

   ```bash
   sudo chown f5xc-service-account:f5xc-operations-group /usr/local/bin/f5xc-backup-restore.py
   ```
