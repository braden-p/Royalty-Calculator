import os
import pandas as pd
from shutil import copyfile

# Create a new folder for summarized statements
processed_folder = 'Publisher_Statement_Summaries'
os.makedirs(processed_folder, exist_ok=True)

# Copy contents of 'Publisher Statements XLSX' to 'Publisher_Statement_Summaries'
for filename in os.listdir('Publisher_Statements_XLSX'):
    source_path = os.path.join('Publisher_Statements_XLSX', filename)
    destination_path = os.path.join(processed_folder, filename)
    copyfile(source_path, destination_path)

# Process each spreadsheet in 'Publisher_Statement_Summaries'
for filename in os.listdir(processed_folder):
    file_path = os.path.join(processed_folder, filename)
    df = pd.read_excel(file_path)

    # Fill NaN values in 'admin' and 'agent' with a placeholder
    df['admin'].fillna('NO_ADMIN', inplace=True)
    df['agent'].fillna('NO_AGENT', inplace=True)

    # Process each unique track grouping
    for _, group in df.groupby(['publisher']):
        # Create a new row for the 'total' balance
        total_row = pd.Series({
            'product-type': 'total',
            'balance': group['balance'].sum(),
            # Add other fields you want to copy here
            'publisher': group['publisher'].iloc[0],
            'admin': group['admin'].iloc[0],
            'agent': group['agent'].iloc[0]
        })

        # Remove original rows
        df = df[df['publisher'] != group['publisher'].iloc[0]]

        # Append the 'total' row to the DataFrame
        df = df.append(total_row, ignore_index=True)

    # Save the processed DataFrame back to the original file
    df.to_excel(file_path, index=False)