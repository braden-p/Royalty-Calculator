import pandas as pd

# Import Licenses Functions
from Licenses_Functions import calculate_rate, calculate_1998_1999_rate, calculate_2000_2001_rate, calculate_2002_2003_rate, calculate_2004_2005_rate, calculate_2006_2022_rate, calculate_rate_period, calculate_net_rate

# Import Excel Files
licenses_df = pd.read_excel('Licenses.xlsx')
sales_df = pd.read_excel('Physical_Sales.xlsx')

# Filter Relevant Columns
sales_filtered = sales_df[['product-type', 'upc', 'net-units']]
licenses_filtered = licenses_df[['upc', 'product-type', 'publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'track-number', 'track-title', 'isrc', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds', 'lock-date', 'penny-rate']]

# Merge Data and Perform Calculations
merged_df = pd.merge(sales_filtered, licenses_filtered, how='inner', on=['upc', 'product-type'])

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

# Create New Excel Spreadsheet
royalty_run_df = merged_df[['publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'upc', 'track-number', 'track-title', 'isrc', 'product-type', 'rate-period', 'share', 'net-rate', 'net-units', 'balance']]
royalty_run_df.to_excel('royalty-run-physical.xlsx', index=False)
