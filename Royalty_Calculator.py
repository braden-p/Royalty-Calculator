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

# Create Publisher Statements
with open("Statement_Maker.py") as make_statements:
    exec(make_statements.read())

# Process Publisher Statements
with open("Statement_Processor.py") as process_statements:
    exec(process_statements.read())

# Create Publisher Statement Summaries
with open("Statement_Summarizer.py") as summarize_statements:
    exec(summarize_statements.read())

# Create Publisher Statement Cover Sheets
with open("Cover_Sheet_Maker.py") as make_cover_sheets:
    exec(make_cover_sheets.read())