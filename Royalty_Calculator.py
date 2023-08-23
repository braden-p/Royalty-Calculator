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
sales_filtered = sales_df[['product-type', 'upc', 'net-units']]
licenses_filtered = licenses_df[['upc', 'product-type', 'publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'track-title', 'isrc', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds', 'penny-rate']]

# Merge Data and Perform Calculations
merged_df = pd.merge(sales_filtered, licenses_filtered, how='inner', on=['upc', 'product-type'])

# Calculate net rate based on rate-type
def calculate_net_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.091
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.091
        else:
            return (row['track-minutes'] + 1) * 0.0175
    elif row['rate-type'] == 'Min Stat':
        return 0.091
    else:
        return None  # Handle unknown rate-types if needed

merged_df['net-rate'] = merged_df.apply(calculate_net_rate, axis=1)

# Calculate balance
def calculate_balance(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate'] * row['net-units']
    else:
        return (row['share'] / 100) * row['net-rate'] * row['net-units']

merged_df['balance'] = merged_df.apply(calculate_balance, axis=1)

# Create New Excel Spreadsheet
royalty_run_df = merged_df[['publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'upc', 'track-title', 'isrc', 'product-type', 'share', 'net-rate', 'net-units', 'balance']]
royalty_run_df.to_excel('royalty-run.xlsx', index=False)
