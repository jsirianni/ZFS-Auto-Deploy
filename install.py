#!/usr/bin/env python
#
# Install ZFS On Linux
#
# Version 0.0.1
# Joseph Sirianni
#


#
# Variables to be used for ZFS configuration
#
zpool_name = "datastore"
number_of_drives = 0
raid_type = "mirror"    # default RAID1


#
# Boolean variables to enable or disable features
#
auto_scrub = False
auto_snapshot = False
gmail_alerts = False


#
# Print Description
#
print("\n\n\n\nThis script will provide a guided setup for ZFS on Linux. Feel free to modify and distribute.")
print("\nTo contribute, visit GITHUBLINKHERE or email me at Joseph.Sirianni88@gmail.com")


#
# Prompt user for zpool name
#
print("\n\n\n\nConfigure ZFS Specifications\n")
zpool_name = raw_input("\nInput Zpool name: ")


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
    raid_type = input("\nInput RAID type: ")

if raid_type == 0:
    selected_raid_type = "raid0"
elif raid_type == 1:
    selected_raid_type = "raid1"
elif raid_type == 2:
    selected_raid_type = "raid10"
elif raid_type == 3:
    selected_raid_type = "raidz1"
elif raid_type == 4:
    selected_raid_type = "raiz2"
elif raid_type == 5:
    selected_raid_type = "raidz3"


#
# Prompt user for drives to use
#
select_drives = True
drive_set_1 = ""
number_of_drives = 0

print("\n\nConfigure hard drives to use for ZFS")
print("Enter each drive one by one. Example: /dev/sdb")
print("Enter 'done' when done selecting drives")

while select_drives == True:
    drive = raw_input("\nEnter drive: ")
    if drive != "done":
        drive_set_1 += (drive + " ")
        number_of_drives += 1
    else:
        #
        # Validate raid type
        #
        if raid_type == 0 and number_of_drives < 2:
            print("\nRAID0 requires at least two drives.")
        if raid_type == 1 and number_of_drives < 2:
            print("\nRAID1 requires at least two drives.")
        elif raid_type == 2 and number_of_drives < 4:
            print("\nRAID10 requires at least four drives.")
        elif raid_type == 3 and number_of_drives < 3:
            print("\nRAIDZ1 requires at least three drives.")
        elif raid_type == 4 and number_of_drives < 4:
            print("\nRAIDZ2 requires at least four drives.")
        elif raid_type == 5 and number_of_drives < 5:
            print("\nRAIDZ3 requires at least five drives.")
        else: # RAID validation passed, continue.
            select_drives = False


#
# Prompt user for feature selection
#
print("\n\n\n\nAnswer True or False to enable or disable features\n")
auto_scrub = input("\nEnable or disable ZFS Auto Scrub: ")
auto_snapshot = input("\nEnable or disable ZFS Auto Snapshots: ")
gmail_alerts = input("\nEnable or Disable Gmail Email Alerts: ")


#
# Print ZFS deployment summary.
#
print("\n\n\n\nZFS Deployment Configuration Summary")
print("\nZpool name: " + zpool_name)
print("Number of drives: " + str(number_of_drives))
print("Drives to use: " + drive_set_1)
print("Raid Type: " + selected_raid_type)

print("\n\nZFS Enabled Features Summary")
if auto_scrub == True:
    print("\nZFS Auto Scrub Enabled")
if auto_snapshot == True:
    print("ZFS Auto Snapshots Enabled")
if gmail_alerts == True:
    print("Gmail Email Alerts Enabled")


#
#  Prompt user for comfirmation
#
verify_config = input("\n\nIs the above configuration correct? Answer True or False: ")
if verify_config == True:
    print("\nInstalling and configuring ZFS\n")
else:
    print("\nUser aborted the setup\n")
