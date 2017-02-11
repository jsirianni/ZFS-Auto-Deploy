zfs-auto-deploy
Joseph Sirianni
12-16-2016
Version 0.5.0



How to install
  - git clone the repo to a directory of your choice (likely /tmp)
  - edit the 'install.sh' script to fit your enviroment
  - make 'install.sh' executable with 'chmod +x install.sh'
  - execute 'install.sh'
  - edit zed.rc file directive 'ZED_EMAIL_ADDRESS' to include the recipient email
  - You will be prompted four times for required information
      - samba password for the samba user "sambauser"
      - samba password comfirmation
      - email alerts sending email address
          - this email is what the system uses to SEND alerts
              - you should use a throw away / dumby email because the password is stored in plain text!!!
      - email password
   

 When the script is finished, you will have your zpool setup, SAMBA configured with 'sambauser' and the password you specified
 The zpool will be mounted in /mnt/data and be fully useable by the samba user.

 You will notice that many features are hardcoded. This will change in future releases to make the script much more dynamic.

 Please send any suggestions to Joseph.Sirianni88@gmail.com


 # BUG LIST #
  - Email alers may not work when zpool changes to 'degraded' mode
