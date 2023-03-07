#!/bin/sh
from ftplib import FTP
from datetime import datetime
import pandas as pd
import numpy as np
import shutil

start = datetime.now()
ftp = FTP('ftp.davidsonsinventory.com')
ftp.login('ftp58074930-1','DavDealerInv')

# Get All Files
files = ftp.nlst()

# Print out the files

print("Downloading...davidsons_quantity.csv")
print("Downloading...davidsons_inventory.csv")
ftp.retrbinary("RETR davidsons_quantity.csv" ,open("./davidsons_quantity.csv", 'wb').write)
ftp.retrbinary("RETR davidsons_inventory.csv" ,open("./davidsons_inventory.csv", 'wb').write)

ftp.close()

end = datetime.now()
diff = end - start
print('All files downloaded for ' + str(diff.seconds) + 's')



df = pd.read_csv("./davidsons_quantity.csv", index_col=False)
df.columns = df.columns.str.strip()

df['Quantity_NC'] = df['Quantity_NC'].replace(['99+'],'99')
df['Quantity_AZ'] = df['Quantity_AZ'].replace(['99+'],'99')
df['Quantity_NC'] = df['Quantity_NC'].replace(['A*'],'0')
df['Quantity_AZ'] = df['Quantity_AZ'].replace(['A*'],'0')
df["Quantity_NC"] = pd.to_numeric(df["Quantity_NC"])
df["Quantity_AZ"] = pd.to_numeric(df["Quantity_AZ"])
df['Total'] = (df['Quantity_NC'] + df['Quantity_AZ'])
df['UPC'] = df['UPC_Code']
df = df[['UPC','Item_Number','Quantity_NC','Quantity_AZ','Total']]
df.to_csv('./DavidsonsInventory.csv', index=False)

# Read in the davidsons_inventory.csv file using Pandas
davidsons_inventory = pd.read_csv("davidsons_inventory.csv")

# Remove leading/trailing whitespaces from the column names
davidsons_inventory.columns = davidsons_inventory.columns.str.strip()

# Removing leading and trailing "#" from the "UPC Code" column
davidsons_inventory["UPC Code"] = davidsons_inventory["UPC Code"].str.replace('#','')

# Read in the DavidsonsInventory.csv file using Pandas
inventory = pd.read_csv("DavidsonsInventory.csv")

# Create a new dataframe with only the "UPC", "Dealer Price" and "Sale Price" columns
new_inventory = inventory.copy()

for index, row in inventory.iterrows():
    # Get the UPC value for the current row
    upc = row["UPC"]
    # Use the .loc[] indexer to select the corresponding row in the davidsons_inventory dataframe
    davidsons_row = davidsons_inventory.loc[davidsons_inventory["UPC Code"] == upc]
    # Check if the UPC code is found in the davidsons_inventory dataframe
    if davidsons_row.empty:
        continue
    else:
        # Add the "Dealer Price" and "Sale Price" columns to the new dataframe
        new_inventory.at[index,"Dealer Price"] = davidsons_row.iloc[0]["Dealer Price"]
        new_inventory.at[index,"Sale Price"] = davidsons_row.iloc[0]["Sale Price"]

# remove the "$" symbol from the "Dealer Price" and "Sale Price" columns
new_inventory["Dealer Price"] = new_inventory["Dealer Price"].str.replace("$", "", regex=False)
new_inventory["Sale Price"] = new_inventory["Sale Price"].str.replace("$", "", regex=False)


new_inventory["Dealer Price"] = new_inventory["Dealer Price"].astype(float)
new_inventory["Sale Price"] = new_inventory["Sale Price"].astype(float)





# Write the new dataframe to a new CSV file
new_inventory.to_csv("DavidsonsInventory.csv", index=False)
print("New DavidsonsInventory.csv file created")



src_path = "./DavidsonsInventory.csv"
dst_path= "./Result/"
shutil.copy(src_path, dst_path)
print("DavidsonsInventory.csv file moved to Result folder")
