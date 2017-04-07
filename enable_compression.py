#!/usr/bin/env python3
import os

#
# This script enables or disables zfs compression
#
# Pass a zpool name or  zpool dataset name as strings
#


'''
Call this function to disable zfs compression
'''
def disable(zpool_name):
    os.system("sudo zfs set compression=off " + zpool_name)



'''
Call this function to enable zfs compression
Supported compression methods: lzjb, lz4, gzip, gzip[1-9], zle
If no compression type is passed, lz4 will be used
'''
def enable(zpool_name, comp_type="lz4"):
    os.system("sudo zfs set compression=" + comp_type + " " + zpool_name)
