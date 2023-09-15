"""
Royalty Calculator
Created by Braden Piper, bradenpiper.com
Created on Aug 21, 2023
Version = 1.0
------------------------------------------
DESCRIPTION:
A mechanical royalty calculation and management software.
"""

import pandas as pd

# Import Excel Files
licenses_df = pd.read_excel('Licenses.xlsx')
physical_sales_df = pd.read_excel('Physical_Sales.xlsx')
digital_album_sales_df = pd.read_excel('Digital_Album_Sales.xlsx')

# Define a mapping dictionary for product types
product_type_mapping = {
    'DA': 'All Digital',
    'DT': 'All Digital'
}

# Create a new column 'merged-product-type' in Digital Sales DataFrames using the mapping
digital_album_sales_df['merged-product-type'] = digital_album_sales_df['product-type'].map(product_type_mapping)
#digital_tracks_sales_df['merged-product-type'] = digital_tracks_sales_df['product-type'].map(product_type_mapping)

# Add a new column 'original-product-type' to Digital Sales DataFrames to store the original product type
digital_album_sales_df['original-product-type'] = digital_album_sales_df['product-type']
#digital_tracks_sales_df['original-product-type'] = digital_tracks_sales_df['product-type']

# Filter Relevant Columns
physical_sales_filtered = physical_sales_df[['product-type', 'upc', 'net-units']]
digital_album_sales_filtered = digital_album_sales_df[['merged-product-type', 'original-product-type', 'upc', 'net-units']]
#digital_tracks_sales_filtered = digital_tracks_sales_df[['merged-product-type', 'original-product-type', 'upc', 'net-units']]
licenses_filtered = licenses_df[['upc', 'product-type', 'publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'track-number', 'track-title', 'isrc', 'share', 'rate-type', 'rate-percent', 'track-minutes', 'track-seconds', 'lock-date', 'penny-rate']]

# Combine Physical and Digital Sales DataFrames
combined_sales_df = pd.concat([physical_sales_filtered, digital_album_sales_filtered], ignore_index=True)

# Merge Data and Perform Calculations
merged_df = pd.merge(combined_sales_df, licenses_filtered, how='inner', left_on=['upc', 'merged-product-type'], right_on=['upc', 'product-type'])

# Calculate rate based on lock-date and rate-type
def calculate_rate(row):
    lock_date = row['lock-date']
    if pd.isnull(lock_date):  # If lock-date is empty, use the 2006-2022 rates
        return calculate_2006_2022_rate(row)
    elif lock_date >= pd.Timestamp(1998, 1, 1) and lock_date <= pd.Timestamp(1999, 12, 31):
        return calculate_1998_1999_rate(row)
    elif lock_date >= pd.Timestamp(2000, 1, 1) and lock_date <= pd.Timestamp(2001, 12, 31):
        return calculate_2000_2001_rate(row)
    elif lock_date >= pd.Timestamp(2002, 1, 1) and lock_date <= pd.Timestamp(2003, 12, 31):
        return calculate_2002_2003_rate(row)
    elif lock_date >= pd.Timestamp(2004, 1, 1) and lock_date <= pd.Timestamp(2005, 12, 31):
        return calculate_2004_2005_rate(row)
    else:
        return calculate_2006_2022_rate(row)

def calculate_1998_1999_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.071 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.071 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0135 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.071 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2000_2001_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.0755 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.0755 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0145 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.0755 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2002_2003_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.08 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.08 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0155 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.08 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2004_2005_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.085 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.085 * (row['rate-percent'] / 100)
        else:
            return (row['track-minutes'] + 1) * 0.0165 * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.085 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

def calculate_2006_2022_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    elif row['rate-type'] == 'Full Stat':
        if row['track-minutes'] < 5:
            return 0.091 * (row['rate-percent'] / 100)
        elif row['track-minutes'] == 5 and row['track-seconds'] == 0:
            return 0.091 * (row['rate-percent'] / 100)
        else:
            return ((row['track-minutes'] + 1) * 0.0175) * (row['rate-percent'] / 100)
    elif row['rate-type'] == 'Min Stat':
        return 0.091 * (row['rate-percent'] / 100)
    else:
        return None  # Handle unknown rate-types if needed

merged_df['rate'] = merged_df.apply(calculate_rate, axis=1)

# Calculate rate-period based on lock-date
def calculate_rate_period(lock_date):
    if lock_date >= pd.Timestamp(1998, 1, 1) and lock_date <= pd.Timestamp(1999, 12, 31):
        return '1998-1999'
    elif lock_date >= pd.Timestamp(2000, 1, 1) and lock_date <= pd.Timestamp(2001, 12, 31):
        return '2000-2001'
    elif lock_date >= pd.Timestamp(2002, 1, 1) and lock_date <= pd.Timestamp(2003, 12, 31):
        return '2002-2003'
    elif lock_date >= pd.Timestamp(2004, 1, 1) and lock_date <= pd.Timestamp(2005, 12, 31):
        return '2004-2005'
    elif lock_date >= pd.Timestamp(2006, 1, 1) and lock_date <= pd.Timestamp(2022, 12, 31):
        return '2006-2022'
    else:
        return None  # No rate-period for empty lock-date or outside specified periods

# Add 'rate-period' column to merged_df
merged_df['rate-period'] = merged_df['lock-date'].apply(calculate_rate_period)

# Calculate net rate
def calculate_net_rate(row):
    if row['rate-type'] == 'Penny Rate':
        return row['penny-rate']
    else:
        return (row['share'] / 100) * row['rate']
    
merged_df['net-rate'] = merged_df.apply(calculate_net_rate, axis=1)

# Calculate balance
def calculate_balance(row):
    return row['net-rate'] * row['net-units']

merged_df['balance'] = merged_df.apply(calculate_balance, axis=1)

# Create New Excel Spreadsheet
royalty_run_df = merged_df[['publisher', 'admin', 'agent', 'album-title', 'catalog-no', 'upc', 'track-number', 'track-title', 'isrc', 'original-product-type', 'merged-product-type', 'rate-period', 'share', 'net-rate', 'net-units', 'balance']]
royalty_run_df.to_excel('royalty-run.xlsx', index=False)

