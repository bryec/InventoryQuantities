import pandas as pd
import numpy as np

# Read in all 4 files
df1 = pd.read_csv("./Result/DavidsonsInventory.csv", dtype={'UPC': str, 'Total': int, 'Dealer Price': float, 'Sale Price': float})
df2 = pd.read_csv("./Result/SportsSouthInventory.csv", dtype={'UPC': str, 'Q': int, 'P': float})
df3 = pd.read_csv("./Result/ZandersInventory.csv", dtype={'upc': str, 'price1': float, 'available': int})
df4 = pd.read_csv("./Result/Lipseys.csv", dtype={'upc': str, 'quantity': int, 'currentPrice': float})
df4 = df4.rename(columns={"upc": "UPC"})


# Create consolidated dataframe with all UPCs from all vendors
df1[['Total']] = df1[['Total']].fillna(0).astype(int)
df2[['Q']] = df2[['Q']].fillna(0).astype(int)
df2[['P']] = df2[['P']].fillna(0).astype(float)
df3[['available']] = df3[['available']].fillna(0).astype(int)
df4[['quantity']] = df4[['quantity']].fillna(0).astype(int)

consolidated = pd.concat([df1['UPC'], df2['UPC'], df3['upc'], df4['UPC']]).drop_duplicates().reset_index(drop=True).to_frame(name='UPC')
consolidated = consolidated.loc[~consolidated["UPC"].duplicated()]

# Merge in quantity and price information from each vendor
consolidated = consolidated.merge(df1[['UPC', 'Total', 'Dealer Price', 'Sale Price']], on='UPC', how='left')
consolidated = consolidated.merge(df2[['UPC', 'Q', 'P']], on='UPC', how='left')
consolidated = consolidated.merge(df3[['upc', 'price1', 'available']], left_on='UPC', right_on='upc', how='left').drop('upc', axis=1)
consolidated = consolidated.merge(df4[['UPC', 'quantity', 'currentPrice']], on='UPC', how='left')

# Fix format for quantities to get rid of decimal places
consolidated['Total'] = consolidated['Total'].apply(lambda x: '{:.0f}'.format(float(x)))
consolidated['Q'] = consolidated['Q'].apply(lambda x: '{:.0f}'.format(float(x)))
consolidated['available'] = consolidated['available'].apply(lambda x: '{:.0f}'.format(float(x)))
consolidated['quantity'] = consolidated['quantity'].apply(lambda x: '{:.0f}'.format(float(x)))


# Rename columns
consolidated = consolidated.rename(columns={
    'Total': 'D-Q',
    'Dealer Price': 'D-P',
    'Sale Price': 'D-SP',
    'Q': 'S-Q',
    'P': 'S-P',
    'price1': 'Z-P',
    'available': 'Z-Q',
    'quantity': 'L-Q',
    'currentPrice': 'L-P'
})


# Remove duplicate UPCs
consolidated = consolidated.loc[~consolidated["UPC"].duplicated()]

# Convert quantity columns to numeric
qty_cols = ['D-Q', 'S-Q', 'Z-Q', 'L-Q']
consolidated[qty_cols] = consolidated[qty_cols].replace(['nan', 'NaN'], np.nan).fillna(0).replace([np.inf, -np.inf], 0).astype(int)


# Remove rows with missing UPC values
consolidated = consolidated.dropna(subset=["UPC"])

# Add 3 additional columns: Best Price, Best Price Vendor and Best Price Quantity
min_cols = ['D-P', 'D-SP', 'S-P', 'Z-P', 'L-P']
consolidated['Best Price'] = consolidated[min_cols].min(axis=1)

def best_price_vendor(row):
    min_price = row['Best Price']
    min_vendor = ''
    for col in min_cols:
        if row[col] == min_price:
            vendor_col = col.split('-')[0] + '-P'
            qty_col = col.split('-')[0] + '-Q'
            if row[qty_col] > 0:
                min_vendor = vendor_col.split('-')[0]
                break
            elif not min_vendor:
                min_vendor = vendor_col.split('-')[0]
    return min_vendor

consolidated['Best Price Vendor'] = consolidated.apply(best_price_vendor, axis=1)

# Write the corresponding quantity to the 'Best Price Quantity' column
def best_price_quantity(row):
    if not all(col in row.index for col in min_cols):
        return 0
    vendor_qty = []
    for col in min_cols:
        if row[col] == row['Best Price']:
            qty_col = col.split('-')[0] + '-Q'
            if qty_col in consolidated.columns:
                if row[qty_col] != 0:
                    vendor_qty.append((col.split('-')[0], row[qty_col]))
    if len(vendor_qty) == 0:
        return 0
    else:
        vendor_qty = sorted(vendor_qty, key=lambda x: x[1])
        return vendor_qty[0][1]

consolidated['Best Price Quantity'] = consolidated.apply(best_price_quantity, axis=1)

# save new file
consolidated['Best Price Vendor'] = consolidated['Best Price Vendor'].replace('Z', 'Zanders').replace('D', 'Davidsons').replace('S', 'SportsSouth').replace('L', 'Lipseys')
consolidated.to_csv('./Result/ConsolidatedInventory.csv', index=False)
