#!/bin/sh



echo "Executing Davidsons.py"
python3 Davidsons.py

echo "Executing SportsSouthInventory.py"
python3 SportsSouthInventory.py

echo "Executing ZandersInventory.py"
python3 ZandersInventory.py

echo "Executing Lipsey.py"
python3 Lipsey.py

echo "Executing mergeinventory.py"
python3 mergeinventory.py

echo "Cleaning up the Result folder"
rm ./Result/ZandersInventory.csv
rm ./Result/SportsSouthInventory.csv
rm ./Result/DavidsonsInventory.csv
rm ./Result/Lipseys.csv

echo "Cleaning up the execution folder"
rm ./davidsons_inventory.csv
rm ./davidsons_quantity.csv
rm ./DavidsonsInventory.csv
rm ./SportsSouthInventory.xml
rm ./ZandersInventory.csv
rm ./zandersinv.csv

cp ./Result/ConsolidatedInventory.csv /var/www/html/wp-content/uploads/wpallimport/files/