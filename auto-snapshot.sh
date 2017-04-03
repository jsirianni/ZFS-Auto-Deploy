#!/bin/bash
cd $(dirname $0)

# Add repo and install auto snapshots
sudo add-apt-repository ppa:bob-ziuchkovski/zfs-auto-snapshot -y
sudo apt-get update
sudo apt-get install -y zfs-auto-snapshot


# Disable top level snapshots & enable weekly, daily, hourly, frequent snapshots for mounted zpool
sudo zfs set com.sun:auto-snapshot=false datastore
sudo zfs set com.sun:auto-snapshot=true datastore/data
sudo zfs set com.sun:auto-snapshot:monthly=false datastore/data
sudo zfs set com.sun:auto-snapshot:weekly=true datastore/data
sudo zfs set com.sun:auto-snapshot:daily=true datastore/data
sudo zfs set com.sun:auto-snapshot:hourly=true datastore/data
sudo zfs set com.sun:auto-snapshot:frequent=false datastore/data
