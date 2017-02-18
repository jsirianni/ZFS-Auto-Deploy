#!/bin/bash
cd $(dirname $0)

# Enable zfs auto scrub - Scrub at 3AM every sunday
sudo mkdir /etc/zfs_scrub
sudo touch /etc/zfs_scrub/scrub.sh
sudo chmod 777 /etc/zfs_scrub/scrub.sh
echo "#!/bin/bash" >> /etc/zfs_scrub/scrub.sh
echo "#When called, this script scrubs the datastore zpool" >> /etc/zfs_scrub/scrub.sh
echo "sudo zpool scrub datastore" >> /etc/zfs_scrub/scrub.sh
line="1 3 * * 7 /etc/zfs_scrub/scrub.sh"
(sudo crontab -u root -l; echo "$line" ) | sudo crontab -u root -
