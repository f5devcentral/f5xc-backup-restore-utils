## Prerequisites

Before you begin, ensure that you have:

- A Linux-based system (such as Red Hat Enterprise Linux or CentOS)
- Administrative privileges on the system
- Internet access to download necessary files

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

5. **Install Required Python Modules**
   The script requires certain Python modules to function. Install them using the `pip` command:

   ```bash
   sudo python3 -m pip install -r requirements.txt
   ```

6. **Set Execution Permissions**
   Make the script executable with the following command:

   ```bash
   chmod +x f5xc-backup-restore.py
   ```

7. **Configure the Script**
   Before running the script, you need to configure it with your F5XC Tenant URL and API Token. Open the script in a text editor and enter your details where required.

8. **Run the Script**
   You can now run the backup or restore script using the following commands:

   ```bash
   ./f5xc-backup-restore.py
   ```
