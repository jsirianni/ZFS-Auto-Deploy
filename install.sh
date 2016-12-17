#!/bin/bash
cd $(dirname $0)
##########################################################################
##########################################################################
# Author: Joe Sirianni unless otherwise stated
# 12-15-2016
# ZFS_Ubuntu16_Deployment v.0.0.1
#
# This script is used to deploy ZFS on linux.
# This script is NOT universal (yet) and requires
# some lines to be hardcoded to the specific
# deployment (zpool creation for example)
#
# Features
#  - ZFS Installatin and configuration    (hardcoded configuration)
#     - Zpool creation and mounting
#     - Zpool auto-snapshots enabled
#     - Zpool auto-scrub enabled
#  - SAMBA installation and configuration (hardcoded configuration)
#  - GMAIL email alerts for ZFS           (Thanks to Josef Jezek)
#  - HTOP & IOTOP for system monitoring
#  - Installation of system updates
#
# Future Features
#  - User input used instead of all hardcoded features
#  - unattended installation
#     - ability to pre-assign variables
#
############################################################################
############################################################################
#
#
#install updates
sudo apt-get update && sudo apt-get -y dist-upgrade
#
#install required software packages
sudo apt-get -y install htop iotop zfsutils-linux samba msmtp-mta ca-certificates heirloom-mailx
#
#create & mount zpool (zpool name and drive selection is hardcoded)
sudo mkdir /mnt/zfs
sudo zpool create -f datastore raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde
sudo zfs create -o mountpoint=/mnt/zfs datastore/data
# Enable zfs auto snapshots
# Weekly snapshots are held for seven weeks
# Daily snapshots are held for 30 days
# Hourly snapshots are held for 24 hours
# This configuration allows for data to be held for seven weeks
sudo add-apt-repository -y ppa:zfs-native/stable; sudo apt-get install -y zfs-auto-snapshot
sudo zfs set com.sun:auto-snapshot=true datastore
sudo zfs set com.sun:auto-snapshot:monthly=false datastore
sudo zfs set com.sun:auto-snapshot:weekly=true datastore
sudo zfs set com.sun:auto-snapshot:daily=true datastore
sudo zfs set com.sun:auto-snapshot:hourly=true datastore
sudo zfs set com.sun:auto-snapshot:frequent=false datastore
#
#
#configure SAMBA network share
echo "***************************************************************"
echo "***************************************************************"
echo
echo "CREATING SAMBA USER FOR NETWORK ACCESS"
echo "PLEASE PROVIDE A PASSWORD"
echo
echo "***************************************************************"
echo "***************************************************************"
sudo adduser sambauser
sudo chown -R sambauser:sambauser /mnt/zfs
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.old
sudo cp smb.conf /etc/samba/smb.conf
(echo password; echo password) | sudo smbpasswd -a sambauser
sudo service smbd restart
sudo service nmbd restart
#
#
##############################################################################
#configure mail alerts
# Sending emails using Gmail and msmtp
# Author: [Josef Jezek](http://about.me/josefjezek)
# Donate: [Gittip](https://www.gittip.com/josefjezek)
# Link: [Gist](https://gist.github.com/6194563)
# Usage: setup-msmtp-for-gmail.sh
###############################################################################
echo "***************************************************************"
echo "***************************************************************"
echo
echo "CONFIGURING EMAIL CLIENT"
echo "PLEASE PROVIDE A VALID EMAIL ADDRESS AND PASSWORD"
echo
echo "***************************************************************"
echo "***************************************************************"
if command -v zenity >/dev/null; then
  GMAIL_USER=$(zenity --entry --title="Gmail username" --text="Enter your gmail username with domain (username@gmail.com):")
  GMAIL_PASS=$(zenity --entry --title="Gmail password" --text="Enter your gmail password:" --hide-text)
else
  read -p "Gmail username with domain (username@gmail.com): " GMAIL_USER
  read -p "Gmail password: " GMAIL_PASS
fi
echo # an empty line
if [ -z "$GMAIL_USER" ]; then echo "No gmail username given. Exiting."; exit -1; fi
if [ -z "$GMAIL_PASS" ]; then echo "No gmail password given. Exiting."; exit -1; fi
sudo tee /etc/msmtprc >/dev/null <<__EOF
# Accounts will inherit settings from this section
defaults
auth            on
tls             on
tls_certcheck   off
# tls_trust_file  /etc/ssl/certs/ca-certificates.crt
logfile /var/log/msmtp.log
# A first gmail address
account   gmail
host      smtp.gmail.com
port      587
from      $GMAIL_USER
user      $GMAIL_USER
password  $GMAIL_PASS
# A second gmail address
account   gmail2 : gmail
from      username@gmail.com
user      username@gmail.com
password  password
# A freemail service
account   freemail
host      smtp.freemail.example
from      joe_smith@freemail.example
user      joe.smith
password  secret
# A provider's service
account   provider
host      smtp.provider.example
# Set a default account
account default : gmail
__EOF
sudo chmod 600 /etc/msmtprc
sudo chown -R www-data:www-data /etc/msmtprc
HOST=$(hostname)
sudo mail -vs "Email relaying configured at ${HOST}" $GMAIL_USER <<__EOF
The postfix service has been configured at host '${HOST}'.
Thank you for using this postfix configuration script.
__EOF
echo "I have sent you a mail to $GMAIL_USER"
echo "This will confirm that the configuration is good."
echo "Please check your inbox at gmail."
###############################################################################
###############################################################################
#
#
# Enable ZFS email alerts
sudo mv /etc/zfs/zed.d/zed.rc /etc/zfs/zed.d/zed.rc.old
sudo cp zed.rc /etc/zfs/zed.d/zed.rc
sudo chown root:root /etc/zfs/zed.d/zed.rc
sudo chmod 600 /etc/zfs/zed.d/zed.rc
sudo chmod +r /etc/zfs/zed.d/zed.rc
sudo service zed enabled
sudo service zed restart
#
# Enable zfs auto scrub - Scrub at 1AM every sunday
sudo mkdir /etc/zfs_scrub
sudo touch /etc/zfs_scrub/scrub.sh
sudo chmod 777 /etc/zfs_scrub/scrub.sh
echo "#!/bin/bash" >> /etc/zfs_scrub/scrub.sh
echo "#When called, this script scrubs the datastore zpool" >> /etc/zfs_scrub/scrub.sh
echo "sudo zpool scrub datastore" >> /etc/zfs_scrub/scrub.sh
line="0 1 * * 0 /etc/zfs_scrub/scrub.sh"
(crontab -u teamit -l; echo "$line" ) | crontab -u teamit -
#
# Reboot
sudo shutdown -r now
#

