import pandas as pd

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

# cast columns ending with "Q" to integers
for col in consolidated.columns:
    if col.endswith('Q'):
        consolidated[col] = consolidated[col].astype(int)

print(consolidated)
