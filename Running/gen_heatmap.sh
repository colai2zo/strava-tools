#!/bin/bash
cd ~/Development/strava-tools/Running

# Ask user if we want to run the scraper
read -p "Run Strava Scraper? (y/n) " scrape
if [ "$scrape" = "y" ]; then
    python3 strava_scraper.py
fi

# Create User Data Folder
cd Data
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
echo "Downloaded $(ls ./user-data | wc -l) GPX files. Converting to pkl."

cd ..
python3 read_files.py
echo "Generated pkl file. Converting to KDS."
Rscript read_data.R
echo "Generated RDS files. Converting to image."
Rscript plot_cosa.R
echo "Converted to png. Done"

