import pandas as pd

# Load the digital_sales_raw.xlsx file into a DataFrame
df = pd.read_excel('Digital_Sales_Raw.xlsx')

# Filter rows where Territory is 'USA'
df = df[df['Territory'] == 'USA']

# Drop the specified columns
columns_to_drop = [
    'Period', 'Activity Period', 'Retailer', 'Territory', 
    "Manufacturer's UPC", 'Product Code', 'Imprint Label', 
    'Track Artist', 'Volume', 'Unit Price', 'Discount', 
    'Actual Price', 'Total', 'Adjusted Total', 'Split Rate', 
    'Label Share Net Receipts', 'Ringtone Publishing', 
    'Cloud Publishing', 'Publishing', 'Mech. Administrative Fee', 
    'Preferred Currency'
]
df.drop(columns=columns_to_drop, inplace=True)

# Rename columns
df.rename(columns={'Orchard UPC': 'upc', 'ISRC': 'isrc', 'Quantity': 'net-units'}, inplace=True)

# Group by all columns and aggregate sum of net-units
digital_sales_grouped = df.groupby(['upc', 'Project Code', 'Artist Name', 'Product Name', 'Track Name', 'isrc','Track #','Trans Type', 'Trans Type Description']).agg({'net-units': 'sum'}).reset_index()

# Create separate DataFrames for Digital Album Sales ('DA') and Digital Track Sales ('DT')
digital_albums_sales = digital_sales_grouped[digital_sales_grouped['Trans Type'] == 'DA']
digital_track_sales = digital_sales_grouped[digital_sales_grouped['Trans Type'] == 'DT']

# Export the processed data to digital_sales_processed.xlsx
digital_albums_sales.to_excel('Digital_Albums_Sales_Processed.xlsx', index=False)
digital_track_sales.to_excel('Digital_Tracks_Sales_Processed.xlsx', index=False)