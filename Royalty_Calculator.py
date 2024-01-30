"""
Royalty Calculator
Created by Braden Piper, bradenpiper.com
Created on Aug 21, 2023
Version = 1.0
------------------------------------------
DESCRIPTION:
A mechanical royalty calculation and management software.
"""

# Process Physical Sales Royalty Run
with open("Physical_Sales_Royalty_Calculator.py") as process_physical:
    exec(process_physical.read())

# Process Digital Album Sales Royalty Run
with open("Digital_Album_Sales_Royalty_Calculator.py") as process_digital_albums:
    exec(process_digital_albums.read())

# Process Digital Track Sales Royalty Run
with open("Digital_Track_Sales_Royalty_Calculator.py") as process_digital_tracks:
    exec(process_digital_tracks.read())

# Load the three ouput Excel files into separate DataFrames
df_digital_albums = pd.read_excel('royalty-run-digital-albums.xlsx')
df_digital_tracks = pd.read_excel('royalty-run-digital-tracks.xlsx')
df_physical = pd.read_excel('royalty-run-physical.xlsx')

# Concatenate the DataFrames vertically
result = pd.concat([df_digital_albums, df_digital_tracks, df_physical])

# Round the 'balance' column to two decimal places
result['balance'] = result['balance'].round(2)

# Sort the data
result = result.sort_values(by=['agent', 'admin', 'publisher', 'track-title', 'album-title'])

# Save the merged DataFrame to a new Excel file
result.to_excel('royalty-run.xlsx', index=False)