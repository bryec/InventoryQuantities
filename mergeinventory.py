import pandas as pd
import numpy as np

# read in all 4 files
df1 = pd.read_csv("./Result/DavidsonsInventory.csv", 
                  usecols=['UPC', 'Total', 'Dealer Price', 'Sale Price'],
                  dtype={'UPC': str, 'Total': int, 'Dealer Price': float, 'Sale Price': float})

df2 = pd.read_csv("./Result/SportsSouthInventory.csv",
                  usecols=['UPC', 'Q', 'P'],
                  dtype={'UPC': str, 'Q': int, 'P': float})

df3 = pd.read_csv("./Result/ZandersInventory.csv", usecols=['upc', 'price1', 'available'], dtype={'upc': str, 'price1': float, 'available': int})
df3 = df3.rename(columns={'upc': 'UPC'})

df4 = pd.read_csv("./Result/Lipseys.csv", dtype={'upc': str, 'quantity': int, 'price': float}, usecols=['upc', 'quantity', 'price'])


# merge all dataframes on UPC
consolidated = pd.merge(df1, df2, on="UPC", how="outer")
consolidated = pd.merge(consolidated, df3, on="UPC", how="outer")
consolidated = pd.merge(consolidated, df4.rename(columns={"upc":"UPC"}), on="UPC", how="outer")

# replace 0 values with NaNs
consolidated = consolidated.replace(0.0, np.nan)

# fill NaNs with 0
consolidated.fillna(0, inplace=True)

# rename columns
consolidated = consolidated.rename(columns={
    "Total": "D-Q",
    "Dealer Price": "D-P",
    "Sale Price": "D-S",
    "Q": "S-Q",
    "P": "S-P",
    "price1": "Z-P",
    "available": "Z-Q",
    "quantity": "L-Q",
    "price": "L-P"
})

# change data types of quantity columns to int
consolidated[['D-Q', 'S-Q', 'Z-Q', 'L-Q']] = consolidated[['D-Q', 'S-Q', 'Z-Q', 'L-Q']].astype(int)

# create a new column 'Best Price' with the lowest available price between all suppliers
consolidated['Best Price'] = consolidated[['D-P', 'S-P', 'Z-P', 'L-P']].min(axis=1)

# create a new column 'Supplier' with the name of the supplier that has the lowest available price
consolidated['Supplier'] = consolidated[['D-P', 'S-P', 'Z-P', 'L-P']].idxmin(axis=1)
consolidated['Supplier'] = consolidated['Supplier'].apply(lambda x: x.split()[0])


# create a new column 'Quantity Available' with the quantity available from the supplier with the lowest available price
def get_quantity_available(row):
    prices = {'Davidsons': row['D-P'], 'SportsSouth': row['S-P'], 'Zanders': row['Z-P'], 'Lipseys': row['L-P']}
    quantities = {'Davidsons': row['D-Q'], 'SportsSouth': row['S-Q'], 'Zanders': row['Z-Q'], 'Lipseys': row['L-Q']}
    min_price = row['Best Price']
    supplier = row['Supplier']
    qty_available = quantities[supplier]
    if qty_available == 0:
        qty_available = min([q for s, q in quantities.items() if prices[s] == min_price])
    return qty_available

consolidated['Quantity Available'] = consolidated.apply(get_quantity_available, axis=1)


print(consolidated.head())


consolidated.to_csv('ConsolidatedInventory.csv', index=False)
