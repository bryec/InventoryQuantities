#!/bin/sh

python3 Davidsons.py
python3 SportsSouthInventory.py
python3 ZandersInventory.py
python3 Lipsey.py
python3 mergeinventory.py
rm ./Result/ZandersInventory.csv
rm ./Result/SportsSouthInventory.csv
rm ./Result/DavidsonsInventory.csv
rm ./Result/Lipseys.csv
rm ./davidsons_inventory.csv
rm ./davidsons_quantity.csv
rm ./DavidsonsInventory.csv
rm ./SportsSouthInventory.xml
rm ./ZandersInventory.csv
rm ./zandersinv.csv
rm ./Lipseys.csv

