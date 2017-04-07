zfs-auto-deploy
Joseph Sirianni
12-16-2016
Version 2.1.0

Supported OS
  - Ubuntu 16.04 w/ default kernel 4.4 (Officially tested)
  - Debian / Ubuntu (Not tested, may work)
  
Prerequisites
  - Package: Sudo, python3
  - Execute as root or sudo user

Features
  - Interactive zfs on linux install
  - Supports creation of multiple datasets
  - ZFS-Auto-Snapshots
    - Enable or disable global snapshots (entire zpool)
    - Enable or disable dataset snapshots, for each dataset.
  - Optional: Setup zfs email alerts
  - Optional: Enable zfs compression
    - Default compression is lz4


How to install
  - Git clone the repo to a directory of your choice (likely /tmp)
  - Make install.py executable with "chmod +x install.py"
  - There is one file that need to be edited
     - zed.rc
        - Configure 'ZED_EMAIL_ADDRESS'
        - Set to the address that should recieve ZFS alerts

  - Execute 'install.py'

  - Please note the following
      - email alerts sending email address
          - this email is what the system uses to SEND alerts
              - you should use a throw away / dumby email because the password is stored in plain text!!!
              
      - It is important to note that the email specified in zed.rc can be a real email address. That is different from the sending email used by gmail-alerts.sh
