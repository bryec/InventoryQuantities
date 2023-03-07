import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

# Set API endpoint and parameters
url = "http://webservices.theshootingwarehouse.com/smart/inventory.asmx/OnhandUpdateDS"
params = {
    "CustomerNumber": "66765", 
    "UserName": "66765", 
    "Password": "75071",  
    "Source": "*"
}

# Download the XML file
print("Downloading...SportsSouthInventory.xml")
response = requests.get(url, params=params)
with open('SportsSouthInventory.xml', 'wb') as f:
    f.write(response.content)

# Convert the 'I' column to integer type when reading the XML file
root = ET.fromstring(response.content)
for child in root.iter('I'):
    child.text = int(child.text)

# Create a DataFrame from the XML file
df = pd.DataFrame(columns=['I', 'Q', 'P'], dtype=int)
for table in root.findall('.//Table'):
    i = int(table.find('I').text)
    q = int(table.find('Q').text)
    p = float(table.find('P').text)
    df = pd.concat([df, pd.DataFrame({'I': i, 'Q': q, 'P': p}, index=[0])], ignore_index=True)


# Read SS_UPC_Reference.csv and set the 'I' column to integer type
print("Reading SS_UPC_Reference.csv to match item numbers to UPC")
upc_ref = pd.read_csv('SS_UPC_Reference.csv', dtype={'I': int, 'UPC':object})



# Merge the two DataFrames using the 'I' column as the key
merged_df = pd.merge(df, upc_ref, on='I')

# Create the 'Result' folder if it doesn't exist
if not os.path.exists('Result'):
   os.makedirs('Result')

# Write the merged DataFrame to 'Result/SportsSouthInventory.csv'
print("New SportsSouthInventory.csv file created in Result folder")
merged_df.to_csv(r'Result/SportsSouthInventory.csv', index = False, header=True)
