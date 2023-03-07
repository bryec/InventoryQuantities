import pandas as pd

# read in all 3 files
df1 = pd.read_csv("./Result/DavidsonsInventory.csv", dtype={'UPC': str, 'Total': int, 'Dealer Price': float, 'Sale Price': float})
df2 = pd.read_csv("./Result/SportsSouthInventory.csv", dtype={'UPC': str, 'Q': int, 'P': float})
df3 = pd.read_csv("./Result/ZandersInventory.csv", dtype={'upc':str,'price1':float,'available':int})
df4 = pd.read_csv("./Result/Lipseys.csv", dtype={'upc': str, 'quantity': int, 'price': float})
print("All 4 files read in from Result folder")

# merge all dataframes on UPC
consolidated = pd.merge(df1, df2, on="UPC", how="outer")
consolidated = pd.merge(consolidated, df3.rename(columns={"upc": "UPC"}), on="UPC", how="outer")
consolidated = pd.merge(consolidated, df4.rename(columns={"upc":"UPC"}), on="UPC", how="outer")
print("Merging all UPCs into a single file")

# remove rows with NaN UPC
consolidated.dropna(subset=['UPC'], inplace=True)
print("Removing duplicate UPCs and rows with empty UPCs")

# fill NaN values in quantity and price columns with 0
cols_to_fill = ['Total', 'Dealer Price', 'Sale Price', 'Q', 'P', 'available', 'price1', 'quantity', 'price']
consolidated[cols_to_fill] = consolidated[cols_to_fill].fillna(0)
# Format Quantity column
consolidated_df['Quantity'] = consolidated_df['Quantity'].apply(lambda x: f'{int(x):,}')

print("Finding the best price and quantities for each UPC")
# group by UPC and find the lowest price
grouped = consolidated.groupby('UPC', as_index=False).agg({'Total': 'max', 'Dealer Price': 'min', 'Sale Price': 'min', 'Q': 'max', 'P': 'min', 'available': 'max', 'price1': 'min', 'quantity': 'max', 'price': 'min'})

# determine which vendor has the lowest price for each UPC
min_cols = ['Dealer Price', 'Sale Price', 'P', 'price1', 'price']
grouped['Best Price'] = grouped[min_cols].min(axis=1)

def best_price_vendor(row):
    for col in min_cols:
        if row[col] == row['Best Price']:
            if col == 'Dealer Price':
                return 'Davidsons'
            elif col == 'Sale Price':
                return 'Davidsons'
            elif col == 'P':
                return 'SportsSouth'
            elif col == 'price1':
                return 'Zanders'
            elif col == 'price':
                return 'Lipseys'
    return 'Davidsons'

grouped['Best Price Vendor'] = grouped.apply(best_price_vendor, axis=1)

# determine the quantity of the lowest price
def best_price_quantity(row):
    q_col = 'Quantity'
    p_col = 'Price'
    
    # Check if Quantity and Price columns exist in the row
    if q_col not in row.index or p_col not in row.index:
        return 0
    
    # Calculate the product of Quantity and Price
    q = row[q_col]
    p = row[p_col]
    pq = q * p
    
    # Check if the result is NaN or infinite
    if pd.isna(pq) or not np.isfinite(pq):
        return 0
    
    return pq

grouped['Best Price Quantity'] = grouped.apply(best_price_quantity, axis=1)
print("Writing new file ConsoliidatedInventory.csv")
# save new file
grouped.to_csv('./Result/ConsolidatedInventory.csv', index=False)
