import pandas as pd
import numpy as np

# Define a function to read in the inventory files with specified data types
def read_inventory_file(filename, dtypes):
    df = pd.read_csv(filename, dtype=dtypes)
    return df

# Define a function to merge all dataframes on UPC
def merge_inventory_dataframes(inventory_dfs):
    consolidated = pd.concat(inventory_dfs, sort=False)
    consolidated.drop_duplicates(subset=['UPC'], inplace=True)
    consolidated.reset_index(drop=True, inplace=True)
    return consolidated

# Define a function to find the best price and quantities for each UPC
def get_best_prices_and_quantities(consolidated):
    # group by UPC and find the lowest price
    grouped = consolidated.groupby('UPC', as_index=False).agg({
        'Total': 'max',
        'Dealer Price': 'min',
        'Sale Price': 'min',
        'Q': 'max',
        'P': 'min',
        'available': 'max',
        'price1': 'min',
        'quantity': 'max',
        'price': 'min'
    })

    # determine which vendor has the lowest price for each UPC
    min_cols = ['Dealer Price', 'Sale Price', 'P', 'price1', 'price']
    grouped['Best Price'] = grouped[min_cols].min(axis=1)

    def best_price_vendor(row):
        for col in min_cols:
            if row[col] == row['Best Price']:
                if col in ['Dealer Price', 'Sale Price']:
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
        q_col = 'quantity'
        p_col = 'Best Price'
        
        # Check if Quantity and Best Price columns exist in the row
        if q_col not in row.index or p_col not in row.index:
            return 0
        
        # Calculate the product of Quantity and Best Price
        q = row[q_col]
        p = row[p_col]
        pq = q * p
        
        # Check if the result is NaN or infinite
        if pd.isna(pq) or not np.isfinite(pq):
            return 0
        
        return pq

    grouped['Best Price Quantity'] = grouped.apply(best_price_quantity, axis=1)
    return grouped

# Define a function to write the consolidated inventory file
def write_consolidated_inventory_file(grouped, output_filename):
    # save new file
    grouped.to_csv(output_filename, index=False)

# Define the main function
def main():
    # Define the input file paths and data types
    inventory_files = [
        {'filename': './Result/DavidsonsInventory.csv', 'dtypes': {'UPC': str, 'Total': int, 'Dealer Price': float, 'Sale Price': float}},
        {'filename': './Result/SportsSouthInventory.csv', 'dtypes': {'UPC': str, 'Q': int, 'P': float}},
        {'filename': './Result/ZandersInventory.csv', 'dtypes': {'upc':str,'price1':float,'available':int}},
        {'filename': './Result/Lipseys.csv', 'dtypes': {'upc': str, 'quantity': int, 'price': float}}
