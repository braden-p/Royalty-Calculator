"""
Royalty Calculator
Created by Braden Piper, bradenpiper.com
Created on Aug 21, 2023
Version = 0.1
------------------------------------------
DESCRIPTION:
A mechanical royalty calculation and management software.
"""

import pandas as pd

# Import Excel Files
licenses_df = pd.read_excel('Licenses.xlsx')
sales_df = pd.read_excel('Physical_Sales.xlsx')

# Filter Relevant Columns
sales_filtered = sales_df[['product-type', 'upc-ean', 'net-units']]
licenses_filtered = licenses_df[['upc', 'product-type', 'publisher', 'album-title', 'catalog-no', 'track-title', 'ISRC', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds']]

# Merge Data and Perform Calculations
merged_df = pd.merge(sales_filtered, licenses_filtered, how='inner', on=['upc', 'product-type'])

# Calculate song length in seconds
merged_df['song-length'] = merged_df['track-minutes'] * 60 + merged_df['track-seconds']

# Calculate net rate based on rate-type and rate-percent
merged_df['net-rate'] = merged_df.apply(lambda row: row['rate-percent'] if row['rate-type'] == 'percentage' else row['penny-rate'], axis=1)

# Calculate balance
merged_df['balance'] = merged_df['share'] * merged_df['net-rate'] * merged_df['net-units']

# Create New Excel Spreadsheet
royalty_run_df = merged_df[['publisher', 'album-title', 'catalog-no', 'upc', 'track-title', 'ISRC', 'product-type', 'share', 'net-rate', 'net-units', 'balance']]
royalty_run_df.to_excel('royalty-run.xlsx', index=False)
