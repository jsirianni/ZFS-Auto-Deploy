#!/usr/bin/env python
import os

#
# Install ZFS On Linux
#
# Version 0.0.1
# Joseph Sirianni
#


#
# Print Description
#
print("\n\n\n\nThis script will provide a guided setup for ZFS on Linux. Feel free to modify and distribute.")
print("\nTo contribute, visit GITHUBLINKHERE or email me at Joseph.Sirianni88@gmail.com")


#
# Prompt user for zpool name
#
print("\n\n\n\nConfigure ZFS Specifications\n")
zpool_name = str(input("\nInput Zpool name: "))


#
# Prompt user for RAID type
#
raid_type = -1
while raid_type < 0 or raid_type > 5:
    print("\n\nSpecify RAID type to be used")
    print("\n0 = raid0 = minimum of two drives")
    print("1 = raid1 = minimum of two drives")
    print("2 = raid10 = minimum of four drives")
    print("3 = raidz1 = minimum of three drives")
    print("4 = raidz2 = minimum of four drives")
    print("5 = raidz3 = minimum of five drives")
    raid_type = int(input("\nInput RAID type: "))

if raid_type == 0:
    selected_raid_type = "raid0"
elif raid_type == 1:
    selected_raid_type = "mirror"
elif raid_type == 2:
    selected_raid_type = "mirror" # ZFS stripes multiple mirros, aka raid10
elif raid_type == 3:
    selected_raid_type = "raidz1"
elif raid_type == 4:
    selected_raid_type = "raiz2"
elif raid_type == 5:
    selected_raid_type = "raidz3"


#
# Prompt user for drives to use
#
drive_set_1 = ""
number_of_drives = 0

print("\n\n\nConfigure hard drives to use for ZFS")
print("\nEnter each drive one by one. Example: /dev/sdb")
print("Enter 'done' when done selecting drives")
print("Enter 'list' if you need a list of drives")

while 1 == 1:
    # Input a drive
    drive = str(input("\nEnter drive: "))

    # Print list of drives if user enters "list"
    if drive == "list":
        os.system("sudo lsblk")
        continue

    # If user enters a drive, add it to the set
    if drive != "done":
        drive_set_1 += (drive + " ")
        number_of_drives += 1
        continue

    # If user enters "done", check if drive list is compatable with raid type
    else:
        if raid_type == 0 and number_of_drives < 2:
            print("\nRAID0 requires at least two drives.")
            continue
        elif raid_type == 1 and number_of_drives < 2:
            print("\nRAID1 requires at least two drives.")
            continue
        elif raid_type == 3 and number_of_drives < 3:
            print("\nRAIDZ1 requires at least three drives.")
            continue
        elif raid_type == 4 and number_of_drives < 4:
            print("\nRAIDZ2 requires at least four drives.")
            continue
        elif raid_type == 5 and number_of_drives < 5:
            print("\nRAIDZ3 requires at least five drives.")
            continue
        elif raid_type == 2 and number_of_drives < 4:
            print("\nRAID10 requires at least four drives.")
            continue
        # If raid10, check if even number of drives
        elif raid_type == 2:
            d = (number_of_drives // 2)
            d = (d * 2)
            if d != number_of_drives:
                print("\nRAID10 requires an even amount of drives")
                continue
            else:
                break
        # If all validation passes, break loop.
        else:
            break


#
# Prompt user for feature selection
#
print("\n\n\n\nAnswer 'True' or 'False' to enable or disable features\n")

create_datasets = input("\nCreate ZFS datasets and mount points? ")
if create_datasets == "True":
    create_datasets = True
else:
    create_datasets = False

auto_scrub = input("\nZFS Auto Scrub: ")
if auto_scrub == "True":
    auto_scrub = True
else:
    auto_scrub = False

auto_snapshot = input("\nZFS Auto Snapshots: ")
if auto_snapshot == "True":
    auto_snapshot = True
else:
    auto_snapshot = False

gmail_alerts = input("\nGmail Email Alerts: ")
if gmail_alerts == "True":
    gmail_alerts = True
else:
    gmail_alerts = False


#
# Print ZFS deployment summary.
#
print("\n\n\n\nZFS Deployment Configuration Summary")
print("\nZpool name: " + zpool_name)
print("Number of drives: " + str(number_of_drives))
print("Drives to use: " + drive_set_1)
print("Raid Type: " + selected_raid_type)

print("\n\nZFS Enabled Features Summary")
if create_datasets == True:
    print("\nDatasets will be created interactively during deployment")
if auto_scrub == True:
    print("ZFS Auto Scrub Enabled")
if auto_snapshot == True:
    print("ZFS Auto Snapshots Enabled")
if gmail_alerts == True:
    print("Gmail Email Alerts Enabled")


#
#  Prompt user for comfirmation
#
verify_config = input("\n\nIs the above configuration correct? Answer True or False: ")
if verify_config == "True":
    verify_config = True
else:
    verify_config = False


#
# Execute configuration
#
if verify_config == True:
    #
    # Run ZFS installer and create zpool
    #
    os.system("sudo apt-get update")
    os.system("sudo apt-get install -y zfsutils-linux")
    os.system("sudo zpool create -f " + zpool_name + " " + selected_raid_type + " " + drive_set_1)

    #
    # Install features
    #
    #
    # Create datasets and mount them
    #
    while create_datasets:
        dataset = str(input("\n\nEnter a dataset name for " + zpool_name + ": "))
        mount_dir = str(input("Enter mount point for " + zpool_name + "/" + dataset + ": "))
        os.system("sudo mkdir " + mount_dir)
        os.system("sudo zfs create -o mountpoint=" + mount_dir + " " + zpool_name + "/" + dataset)
        create_more_datasets = input("\nCreate another dataset? Enter True or False: ")
        if create_more_datasets != "True":
            break
    #
    # Execute auto scrub script`
    #
    if auto_scrub == True:
        os.system("sudo sh auto-scrub.sh")

    if auto_snapshot == True:
        os.system("sudo sh auto-snapshot.sh")

    #
    # Execute email alerts interactvie script
    #
    if gmail_alerts == True:
        os.system("sudo sh gmail-alerts.sh")


#
# User did not commit to configuration, abort`
#
else:
    print("\nUser aborted the setup\n")
