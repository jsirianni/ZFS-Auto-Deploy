#!/usr/bin/env python3
import os

#
# This script interactively sets up zfs snapshots
#
# Pass a zpool name and zpool dataset name as strings
#

'''
Call this function to install zfs-auto-snapshots
'''
def install():
    os.system("wget https://github.com/jsirianni/zfs-autosnapshots-deb/raw/master/zfs-auto-snapshot-trustyport.deb -P /tmp")
    os.system("dpkg -i /tmp/zfs-auto-snapshot-trustyport.deb")


'''
Call this function when you want to disable all snapshots on a given zpool.
Pass either the zpool name or the zpool/dataset as a string.

First snapshots are set to 'true', then each snapshot type is set to false.
This allows us to enable dataset snapshots after disabling top level snapshots.
'''
def disable(zpool_name):
    os.system("sudo zfs set com.sun:auto-snapshot=true " + zpool_name)
    os.system("sudo zfs set com.sun:auto-snapshot:monthly=false " + zpool_name)
    os.system("sudo zfs set com.sun:auto-snapshot:weekly=false " + zpool_name)
    os.system("sudo zfs set com.sun:auto-snapshot:daily=false " + zpool_name)
    os.system("sudo zfs set com.sun:auto-snapshot:hourly=false " + zpool_name)
    os.system("sudo zfs set com.sun:auto-snapshot:frequent=false " + zpool_name)


'''
Call this function when you want to setup snapshots
Pass a string with either the zpool name or the zpoolname and dataset.
'''
def enable(zpool_name):
    print("\n\nSetting up ZFS snapshots. Enter 'y' or 'n' at each prompt")
    print("Setup will enable/disable; frequent, hourly, daily, weekly, and monthly snapshots")

    # Enable snapshots in general
    os.system("sudo zfs set com.sun:auto-snapshot=true " + zpool_name)

    # frequent snapshots. Every 15min, retain last four snapshots
    if input("\nEnable frequent snapshots (Every 15min, retaining the last four snapshots)? ") == "y":
        os.system("sudo zfs set com.sun:auto-snapshot:frequent=true " + zpool_name)
        print("Frequent snapshots enabled for " + zpool_name)
    else:
        os.system("sudo zfs set com.sun:auto-snapshot:frequent=false " + zpool_name)

    # Hourly snapshots, retain last 24 snapshots
    if input("\nEnable hourly snapshots (Every hour, retaining the last 24 snapshots)? ") == "y":
        os.system("sudo zfs set com.sun:auto-snapshot:hourly=true " + zpool_name)
        print("Hourly snapshots enabled for " + zpool_name)
    else:
        os.system("sudo zfs set com.sun:auto-snapshot:hourly=false " + zpool_name)

    # Daily snapshots, retain last 31 snapshots
    if input("\nEnable daily snapshots (Every day, retaining the last 31 snapshots)? ") == "y":
        os.system("sudo zfs set com.sun:auto-snapshot:daily=true " + zpool_name)
        print("Daily snapshots enabled for " + zpool_name)
    else:
        os.system("sudo zfs set com.sun:auto-snapshot:daily=false " + zpool_name)

    # Weekly snapshots, retain last 7 snapshots
    if input("\nEnable weekly snapshots (Every week, retaining the last 7 snapshots)? ") == "y":
        os.system("sudo zfs set com.sun:auto-snapshot:weekly=true " + zpool_name)
        print("Weekly snapshots enabled for " + zpool_name)
    else:
        os.system("sudo zfs set com.sun:auto-snapshot:weekly=false " + zpool_name)

    # Monthly snapshots, retain last 12 snapshots
    if input("\nEnable monthly snapshots (Every monthly, retaining the last 12 snapshots)? ") == "y":
        os.system("sudo zfs set com.sun:auto-snapshot:monthly=true " + zpool_name)
        print("Monthly snapshots enabled for " + zpool_name)
    else:
        os.system("sudo zfs set com.sun:auto-snapshot:monthly=false " + zpool_name)
