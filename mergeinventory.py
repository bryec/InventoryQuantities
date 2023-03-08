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

# remove rows with NaN UPC
consolidated.dropna(subset=['UPC'], inplace=True)



# fill NaN values in quantity and price columns with 0
cols_to_fill = ['Total', 'Dealer Price', 'Sale Price', 'Q', 'P', 'available', 'price1', 'quantity', 'price']
cols_to_int = ['Total', 'Q', 'available', 'quantity']
consolidated[cols_to_fill] = consolidated[cols_to_fill].fillna(0)
consolidated[cols_to_int] = consolidated[cols_to_int].astype(int)



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
                return 'SportsSouth'
            elif col == 'P':
                return 'SportsSouth'
            elif col == 'price1':
                return 'Zanders'
            elif col == 'price':
                return 'Lipseys'
    return 'Davidsons'

grouped['Best Price Vendor'] = grouped.apply(best_price_vendor, axis=1)
print(grouped.head(20))
# determine the quantity of the lowest price
def best_price_quantity(row):
    for col in min_cols:
        if row[col] == row['Best Price']:
            q_col = col[0] + '-Q'
            return row[q_col]
    return 0

grouped['Best Price Quantity'] = grouped.apply(best_price_quantity, axis=1)

# format the output
output = grouped[['UPC', 'Best Price', 'Best Price Vendor', 'Best Price Quantity']]
output.columns = ['UPC', 'Price', 'Vendor', 'Quantity']

# save new file
output.to_csv('./Result/ConsolidatedInventory.csv', index=False)
