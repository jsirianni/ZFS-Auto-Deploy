# zfs-auto-deploy
# Joseph Sirianni
# 12-16-2016

Deploy ZFS on Linux + SAMBA

The purpose of this script is to make installing ZoL (ZFS on Linux), SAMBA (native file sharing for Windows enviroments)
and email alerts much easier. Currently the script is hardcoded to fit specific use cases, however in the future I plan
to add the abilty to configure a "setup" file with variables such as "hostname, zfs raid type, numbers of drives, samba
user name, email alert username, and so on". 

The current version is v0.0.1. The scirpt fits a specific use case that I currently need but could easily be adopted to 
fit other enviroments. It simply makes deploying ZFS + SAMBA with email alerts much easier than going command by command.


How to install
  - git clone the repo to a directory of your choice (likely /tmp)
  - edit the 'install.sh' script to fit your enviroment
  - make 'install.sh' executable with 'chmod +x install.sh'
  - execute 'install.sh'
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
 zfs auto snapshots do not work
  - this is an easy fix. Expect auto snapshots to be fully supported in v0.0.2
  
  zfs auto scrub does not work
   - another easy fix. Expect it to be fully supported in v0.0.2
   
   
