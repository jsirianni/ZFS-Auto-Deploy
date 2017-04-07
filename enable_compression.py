#!/usr/bin/env python3
import os

#
# This script enables or disables zfs compression
#
# Pass a zpool name or  zpool dataset name as strings
#



def disable(zpool_name):
    '''
    Call this function to disable zfs compression.
    '''
    os.system("sudo zfs set compression=off " + zpool_name)



def enable(zpool_name, comp_type="lz4"):
    '''
    Call this function to enable zfs compression.
    '''
    os.system("sudo zfs set compression=lz4 " + zpool_name)



def validate(comp_type):
    '''
    Call this function to validate the selected compression type.
    Supported compression methods: lzjb, lz4, gzip.
    This function returns a boolean value.
    '''
    if comp_type == "lzjb" or "lz4" or "gzip":
        return True

    if comp_type == "off" or "":
        return False
