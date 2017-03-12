#!/usr/bin/env python
import os
import auto-snapshot
#
# Install ZFS On Linux
#
# Version 0.5.1
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
print("\nEnter each drive one by one with the format shown. Example: /dev/sdb")
print("Enter 'done' when done selecting drives")
print("Enter 'list' if you need a list of drives")

while 1 == 1:
    # Input a drive. Trim whitespace
    drive = str(input("\nEnter drive: "))
    drive = drive.strip()

    # Check for blank input
    if drive == "":
        print("You cannot enter a blank drive. Input 'done' to end drive selection")

    # Print list of drives if user enters "list"
    if drive == "list":
        os.system("sudo lsblk")
        continue

    # If user enters a drive, add it to the set
    if drive != "done":
        drive_set_1 += (drive + " ")
        number_of_drives += 1
        continue

    # If user enters done, validate drive number requirement
    elif drive == "done":
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
    datasets = []
    while create_datasets:
        dataset = str(input("\n\nEnter a dataset name for " + zpool_name + ": "))
        datasets.append(dataset)
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

    #
    # Configure zfs snapshots
    #
    if auto_snapshot == True:
        # Setup required repos
        os.system("sudo add-apt-repository ppa:bob-ziuchkovski/zfs-auto-snapshot -y")
        os.system("sudo apt-get update")
        os.system("sudo apt-get install -y zfs-auto-snapshot")

        # Setup zpool global snapshots (all datasets)
        print("Setup zpool level (global) snapshots. Global snapshots will")
        print("take a snapshot of the entire zpool (including all datasets)")
        print("It is usually recomended to setup snapshots per dataset and leave ")
        print("global snapshots disabled")
        global_snapshots = input("\nSetup zpool level snapshots? 'True' or 'False': ")
        if global_snapshots = "True":
            auto-snapshot.global_snapshots(zpool_name)
        else:
            auto-snapshot.disable(zpool_name)

        # Setup dataset level snapshots
        dataset_snapshots = input("\nSetup snapshots for each dataset? 'True' or 'False'?: ")
        if dataset_snapshots = "True":

            # Iterate through dataset list and setup snapshots
            for dataset in datasets:
                dataset = zpool_name + "/" + dataset
                response = input("\nSetup snapshots for " dataset " dataset?")
                if response == "True":
                    auto-snapshot.global_snapshots(dataset)
                else:
                    auto-snapshot.disable(dataset)

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
