#!/usr/bin/env python3
import os
import auto_snapshot
import enable_compression



#
# Interactive ZFS on Linux setup
#



#
# Print Description
#
os.system("clear")
print("This script will provide a guided setup for ZFS on Linux. Feel free to modify and distribute.")
print("To contribute, visit 'https://github.com/jsirianni/zfs-auto-deploy' or email me at Joseph.Sirianni88@gmail.com")



#
# Get zpool name
#
zpool_name = str(input("\nInput zpool name: "))



#
# Get raid_type
#
raid_type = -1
while raid_type < 0 or raid_type > 5:
    print("\nSpecify RAID type to be used")
    print("0 = raid0 = minimum of two drives")
    print("1 = raid1 = minimum of two drives")
    print("2 = raid10 = minimum of four drives")
    print("3 = raidz1 = minimum of three drives")
    print("4 = raidz2 = minimum of four drives")
    print("5 = raidz3 = minimum of five drives")
    raid_type = int(input("\nInput RAID type: "))



#
# Determine ZFS RAID type
#
if raid_type == 0:
    selected_raid_type = "raid0"
elif raid_type == 1:
    selected_raid_type = "mirror"
elif raid_type == 2:
    selected_raid_type = "mirror" # ZFS stripes multiple vdevs, aka raid10
elif raid_type == 3:
    selected_raid_type = "raidz1"
elif raid_type == 4:
    selected_raid_type = "raiz2"
elif raid_type == 5:
    selected_raid_type = "raidz3"



#
# Get drive selection
#
drive_set_1 = ""
number_of_drives = 0

print("\nConfigure hard drives to use for ZFS")
print("Enter each drive one by one with the format shown. Example: /dev/sdb")
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
# Clear screan, get feature selection
#
os.system("clear")

if input("\nSetup datasets? Y/N: ") == "y":
    create_datasets = True
else:
    create_datasets = False

if input("Setup auto snapshots? Y/N: ") == "y":
    enable_auto_snapshots = True
else:
    enable_auto_snapshots = False

if input("Setup Compression? Y/N: ") == "y":
    enable_zfs_compression = True
else:
    enable_zfs_compression = False

if input("Setup Gmail Email Alerts? Y/N: ") == "y":
    gmail_alerts = True
else:
    gmail_alerts = False



#
# Print ZFS deployment summary.
#
os.system("clear")

print("ZFS Deployment Configuration Summary\n")
print("Zpool name: " + zpool_name)
print("Number of drives: " + str(number_of_drives))
print("Drives to use: " + drive_set_1)
print("RAID Type: " + selected_raid_type)

if create_datasets == True:
    print("Datasets will be created interactively")

if enable_auto_snapshots == True:
    print("ZFS Auto Snapshots will be configured interactively")

if enable_zfs_compression == True:
    print("ZFS compression will be configured interactively")

if gmail_alerts == True:
    print("Gmail Email Alerts will be configured interactively")



'''
Get comfirmation to installs
'''
if input("\n\nIs the above configuration correct? Y/N: ") == "y":
    #
    # Update repos and install zfsutils-linux
    #
    os.system("sudo apt-get update")
    os.system("sudo apt-get install -y zfsutils-linux unzip")



    #
    # Create zpool
    #
    os.system("sudo zpool create -f " + zpool_name + " " + selected_raid_type + " " + drive_set_1)
    os.system("clear")



    #
    # Create datasets and mount them
    #
    datasets = []
    while create_datasets == True:
        dataset = str(input("Enter a dataset name for zpool " + zpool_name + ": "))
        datasets.append(dataset)
        mount_dir = str(input("Enter mount point for " + zpool_name + "/" + dataset + ": "))
        os.system("sudo mkdir " + mount_dir)
        os.system("sudo zfs create -o mountpoint=" + mount_dir + " " + zpool_name + "/" + dataset)
        if input("\nCreate another dataset? Y/N: ") != "y":
            os.system("clear")
            break



    #
    # Configure zfs snapshots
    #
    if enable_auto_snapshots == True:
        #
        # Call install function
        #
        auto_snapshot.install()
        os.system("clear")

        #
        # Setup zpool global snapshots (all datasets)
        #
        if input("Setup zpool (global) snapshots? Y/N: ") == "y":
            auto_snapshot.enable(zpool_name)
        else:
            auto_snapshot.disable(zpool_name)

        #
        # Setup dataset level snapshots
        #
        if input("Setup snapshots for each dataset? Y/N: ") == "y":
            # Iterate through dataset list and setup snapshots
            for i in datasets:
                i = (zpool_name + "/" + i)
                if input("Setup snapshots for " + i + " dataset? Y/N: ") == "y":
                    auto_snapshot.enable(i)
                else:
                    auto_snapshot.disable(i)



    #
    # Configure ZFS Compression. Compression is off by default.
    #
    os.system("clear")
    if enable_zfs_compression == True:
        if input("Enable compression on entire zpool, and all datasets? Y/N: ") == "y":
            enable_compression.enable(zpool_name)
        else:
            enable_compression.disable(zpool_name)

        if input("Enable compression per dataset? Y/N: ") == "y":
            for i in datasets:
                n = (zpool_name + "/" + i)
                if input("Enable compression for " + i + " dataset? Y/N: ") == "y":
                    enable_compression.enable(n)
                else:
                    enable_compression.disable(n)



    #
    # Execute email alerts interactvie script
    #
    os.system("clear")
    if gmail_alerts == True:
        os.system("sudo sh gmail-alerts.sh")



    #
    # End Program
    #
    os.system("clear")
    print("zfs-auto-desploy has finished. Please report any bugs!")



#
# User did not commit to configuration, abort`
#
else:
    os.system("clear")
    print("User aborted the setup")
