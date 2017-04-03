#!/usr/bin/env python
import os

#
# This script interactively sets up zfs snapshots
#
# Pass a zpool name and zpool dataset name as strings
#


'''Call this function when you want to setup snapshots
Pass a string with either the zpool name or the zpoolname and dataset.'''

def global_snapshots("zpool_name"):

    print("\n\nSetting up ZFS snapshots. Enter 'True' or 'False' at each prompt")


def disable("zpool_name"):
    os.system("sudo zfs set com.sun:auto-snapshot:monthly=false datastore/data")
    sudo zfs set com.sun:auto-snapshot:weekly=true datastore/data
    sudo zfs set com.sun:auto-snapshot:daily=true datastore/data
    sudo zfs set com.sun:auto-snapshot:hourly=true datastore/data
    sudo zfs set com.sun:auto-snapshot:frequent=false datastore/data
