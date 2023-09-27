import pandas as pd

# Import Licenses Functions
from Licenses_Functions import calculate_rate, calculate_1998_1999_rate, calculate_2000_2001_rate, calculate_2002_2003_rate, calculate_2004_2005_rate, calculate_2006_2022_rate
from Licenses_Functions import calculate_rate_period, calculate_net_rate

# Import Excel Files
licenses_df = pd.read_excel('Licenses.xlsx')
sales_df = pd.read_excel('Digital_Album_Sales.xlsx')

# Filter Relevant Columns in Sales Data
sales_filtered = sales_df[['upc', 'net-units']]

# Filter Rows in Licenses Data where product-type is "All Digital"
licenses_filtered = licenses_df[licenses_df['product-type'] == 'All Digital'][['upc', 'product-type', 'publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'track-number', 'track-title', 'isrc', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds', 'lock-date', 'penny-rate']]

# Merge Data and Perform Calculations
merged_df = pd.merge(sales_filtered, licenses_filtered, how='inner', on=['upc'])

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

# Create Royalty Run Dataframe
royalty_run_df = merged_df[['publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'upc', 'track-number', 'track-title', 'isrc', 'product-type', 'rate-period', 'share', 'net-rate', 'net-units', 'balance']]

# Filter rows with net-units greater than 0
royalty_run_df = royalty_run_df[royalty_run_df['net-units'] > 0]

# Output to Excel
royalty_run_df.to_excel('royalty-run-digital-albums.xlsx', index=False)
