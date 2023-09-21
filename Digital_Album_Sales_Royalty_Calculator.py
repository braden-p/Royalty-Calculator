import pandas as pd

# Import Licenses Functions
from Licenses_Functions import calculate_rate, calculate_1998_1999_rate, calculate_2000_2001_rate, calculate_2002_2003_rate, calculate_2004_2005_rate, calculate_2006_2022_rate
from Licenses_Functions import calculate_rate_period, calculate_net_rate

# Import Excel Files
licenses_df = pd.read_excel('Licenses.xlsx')
sales_df = pd.read_excel('Digital_Album_Sales.xlsx')

# Define a mapping dictionary for product types
product_type_mapping = {
    'DA': 'All Digital',
}

# Create a new column 'merged_product_type' in Digital Sales DataFrames using the mapping
sales_df['merged-product-type'] = sales_df['product-type'].map(product_type_mapping)

# Add a new column 'original_product_type' to Digital Sales DataFrames to store the original product type
sales_df['original-product-type'] = sales_df['product-type']

# Filter Relevant Columns
sales_filtered = sales_df[['merged-product-type', 'original-product-type','upc', 'net-units']]
licenses_filtered = licenses_df[['upc', 'product-type', 'publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'track-number', 'track-title', 'isrc', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds', 'lock-date', 'penny-rate']]

# Merge Data and Perform Calculations
merged_df = pd.merge(sales_filtered, licenses_filtered, how='inner', left_on=['upc', 'merged-product-type'], right_on=['upc', 'product-type'])

# Calculate rate based on lock-date and rate-type
merged_df['rate'] = merged_df.apply(calculate_rate, axis=1)

# Add 'rate-period' column to merged_df
merged_df['rate-period'] = merged_df['lock-date'].apply(calculate_rate_period)

# Calculate net rate
merged_df['net-rate'] = merged_df.apply(calculate_net_rate, axis=1)

# Calculate balance
def calculate_balance(row):
    return row['net-rate'] * row['net-units']

merged_df['balance'] = merged_df.apply(calculate_balance, axis=1)

# Convert "product-type" column to "DA"
merged_df['product-type'] = 'DA'

# Create New Excel Spreadsheet
royalty_run_df = merged_df[['publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'upc', 'track-number', 'track-title', 'isrc', 'product-type', 'rate-period', 'share', 'net-rate', 'net-units', 'balance']]
royalty_run_df.to_excel('royalty-run-digital-albums.xlsx', index=False)
