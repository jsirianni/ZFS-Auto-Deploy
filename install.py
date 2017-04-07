#!/usr/bin/env python3
import os
import auto_snapshot
import enable_compression

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
print("\nTo contribute, visit 'https://github.com/jsirianni/zfs-auto-deploy' or email me at Joseph.Sirianni88@gmail.com")
print("\nUser input should be either y (yes) or n (no) unless otherwise specified")



#
# User inputs zpool name
#
print("\n\n\n\nConfigure ZFS Specifications\n")
zpool_name = str(input("\nInput Zpool name: "))



#
# Prompt the user for the raid type
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
# Prompt user for feature selection. Set boolean flags for feature enable/disable
#
print("\n\n\n\nAnswer 'y' or 'n' to enable or disable features\n")

if input("\nCreate ZFS datasets and mount points? ") == "y":
    create_datasets = True
else:
    create_datasets = False

#if input("\nEnable ZFS Auto Scrub? ") == "y":
#    auto_scrub = True
#else:
#    auto_scrub = False

if input("\nEnable ZFS Auto Snapshots? ") == "y":
    enable_auto_snapshots = True
else:
    enable_auto_snapshots = False

if input("\nEnable ZFS Compression? ") == "y":
    enable_zfs_compression = True
else:
    enable_zfs_compression = False

if input("\nEnable Gmail Email Alerts? ") == "y":
    gmail_alerts = True
else:
    gmail_alerts = False



#
# Print ZFS deployment summary.
#
os.system("clear")
print("\n\n\n\nZFS Deployment Configuration Summary")
print("\nZpool name: " + zpool_name)
print("Number of drives: " + str(number_of_drives))
print("Drives to use: " + drive_set_1)
print("Raid Type: " + selected_raid_type)

print("\n\nZFS Enabled Features Summary")
if create_datasets == True:
    print("\n# Datasets will be created interactively during deployment")
#if auto_scrub == True:
#    print("# ZFS Auto Scrub Enabled")
if enable_auto_snapshots == True:
    print("# ZFS Auto Snapshots Enabled")
if enable_zfs_compression == True:
    print("# ZFS Compression Enabled")
if gmail_alerts == True:
    print("# Gmail Email Alerts Enabled")



#
# Prompt user for comfirmation, execute if true
#
if input("\n\nIs the above configuration correct? Answer 'y' or 'n': ") == "y":

    #
    # Update repos and install zfsutils-linux
    #
    os.system("sudo apt-get update")
    os.system("sudo apt-get install -y zfsutils-linux")
    os.system("clear")

    #
    # Create zpool
    #
    os.system("sudo zpool create -f " + zpool_name + " " + selected_raid_type + " " + drive_set_1)

    #
    # Create datasets and mount them
    #
    datasets = []
    while create_datasets == True:
        dataset = str(input("\n\nEnter a dataset name for zpool " + zpool_name + ": "))
        datasets.append(dataset)
        mount_dir = str(input("Enter mount point for " + zpool_name + "/" + dataset + ": "))
        os.system("sudo mkdir " + mount_dir)
        os.system("sudo zfs create -o mountpoint=" + mount_dir + " " + zpool_name + "/" + dataset)
        if input("\nCreate another dataset? Enter 'y' or 'n': ") != "y":
            break


    #
    # Execute auto scrub script`
    #
    #if auto_scrub == True:
    #    os.system("sudo sh auto-scrub.sh")


    #
    # Configure zfs snapshots
    #
    if enable_auto_snapshots == True:
        # Install auto-snapshots
        auto_snapshot.install()

        # Setup zpool global snapshots (all datasets)
        print("\n\nSetup zpool level (global) snapshots. Global snapshots will take a snapshot of the entire zpool (including all datasets). It is usually recomended to setup snapshots per dataset and leave global snapshots disabled")

        if input("\nSetup zpool (global) snapshots? 'y' or 'n': ") == "y":
            auto_snapshot.enable(zpool_name)
        else:
            auto_snapshot.disable(zpool_name)

        # Setup dataset level snapshots
        if input("\nSetup snapshots for each dataset? 'y' or 'n': ") == "y":
            # Iterate through dataset list and setup snapshots
            for i in datasets:
                i = (zpool_name + "/" + i)
                if input("\nSetup snapshots for " + i + " dataset?: ") == "y":
                    auto_snapshot.enable(i)
                else:
                    auto_snapshot.disable(i)

    #
    # Configure ZFS Compression. Compression is off by default.
    #
    if enable_zfs_compression == True:
        if input("\n\nEnable compression on entire zpool, and all datasets?: " ) == "y":
            enable_compression.enable(zpool_name)
        else:
            enable_compression.disable(zpool_name)

        if input("\n\nEnable compression per dataset?: ") == "y":
            for i in datasets:
                i = (zpool_name + "/" + i)
                if input("\nSetup snapshots for " + i + " dataset?: ") == "y":
                    enable_compression.enable(zpool_name)
                else:
                    enable_compression.disable(zpool_name)

    #
    # Execute email alerts interactvie script
    #
    if gmail_alerts == True:
        os.system("sudo sh gmail-alerts.sh")

    #
    # End Program
    #
    os.system("clear")
    print("\nzfs-auto-desploy has finished. Please report any bugs!")

#
# User did not commit to configuration, abort`
#
else:
    os.system("clear")
    print("\n\nUser aborted the setup\n")
