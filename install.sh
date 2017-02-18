#!/bin/bash
cd $(dirname $0)
# Version 1.0.0

#
# Important: Edit ZPOOL CREATION section to fit
# your enviroment. These lines are commented by default`
#
# Uncomment optional fields to enable each each feature
#


# Update repos and install updates
sudo apt-get update && sudo apt-get -y dist-upgrade

#install required software packages
sudo apt-get -y install zfsutils-linux


##########################
# ZPOOL CREATION         #
# CREATE AND MOUNT zpool #
# EDIT THESE LINES       #
##########################
# Create a directory to mount the zpool to
sudo mkdir /mnt/zfs

# Create a zpool. Edit this line to reflect your requirements
sudo zpool create -f datastore raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde

# Mount the zpool. Notice that datastore/data creates "partition"
sudo zfs create -o mountpoint=/mnt/zfs datastore/data


##########################
# OPTIONAL FEATURES      #
# UNCOMMENT TO USE       #
##########################
# sudo sh auto-snapshot.sh
# sudo sh auto-scrub.sh
# sudo sh gmail-alerts.sh
