zfs-auto-deploy
Joseph Sirianni
12-16-2016
Version 2.0.0

Supported OS
  - Ubuntu 16.04 w/ default kernel 4.4 (Officially tested)
  - Debian / Ubuntu (Not tested, may work)
  
Prerequisites
  - Package: Sudo
  - Execute as root or sudo user

Features
  - Install zfs on linux
  - Optional: Install zfs auto snapshots
  - Optional: Setup zfs auto scrub
  - Optional: Setup zfs email alerts


How to install
  - git clone the repo to a directory of your choice (likely /tmp)
  - edit the 'install.sh' script to fit your enviroment
    - There are four files that need to be edited
      - install.sh
        - Configure mount directory
        - Configure raid type
        - Configure drives to use
        - Configure zpool name and mount location
     - auto-scrub.sh
        - Configure cron job interval
     - auto-snapshot.sh
        - Configure datastore name
        - Enable or disable snapshot types
     - zed.rc
        - Configure 'ZED_EMAIL_ADDRESS'

  - make 'install.sh' executable with 'chmod +x install.sh'
  - execute 'install.sh'

  - You will be prompted for sending email information
      - email alerts sending email address
          - this email is what the system uses to SEND alerts
              - you should use a throw away / dumby email because the password is stored in plain text!!!
      - email password
      - It is important to note that the email specified in zed.rc can be a real email address. That is different from the sending email used by gmail-alerts.sh
