#!/bin/bash
cd ~/Development/strava-tools/Running/Data

# Create User Data Folder
if [ ! -d "./user-data" ]; then
    mkdir "./user-data"
else
    mv user-data user-data-backup
fi

# Download the activity files
for l in $(cat activity_links.txt); do 
    fname="./user-data/$(echo $l | awk -F'/' '{print $NF}').gpx"
    curl "$l/export_gpx" -o $fname
    # If it is not an xml file, delete it
    if head -1 $fname | grep -ivq "xml"; then
        rm -f $fname
    fi
done
