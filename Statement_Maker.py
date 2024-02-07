import os
import pandas as pd

# Read the royalty-run spreadsheet
royalty_run_df = pd.read_excel('royalty-run.xlsx')

# Create a folder for individual publisher statements
output_folder = 'Publisher_Statements_XLSX'
os.makedirs(output_folder, exist_ok=True)

# Filter rows with agent information and save to "Harry Fox Agency"
harry_fox_agency_df = royalty_run_df[royalty_run_df['agent'].notnull()]
harry_fox_agency_df.to_excel(os.path.join(output_folder, 'AGENT-Harry Fox Agency.xlsx'), index=False)

# Filter rows with admin information and save individual spreadsheets
admin_data = royalty_run_df[(royalty_run_df['admin'].notnull()) & (royalty_run_df['agent'].isnull())]
unique_admins = admin_data['admin'].unique()

for admin in unique_admins:
    admin_df = admin_data[admin_data['admin'] == admin]
    admin_df.to_excel(os.path.join(output_folder, f'ADMIN_{admin.replace("/", "_")}.xlsx'), index=False)

# Filter rows without admin or agent and save individual publisher spreadsheets
remaining_publishers_df = royalty_run_df[royalty_run_df['admin'].isnull() & royalty_run_df['agent'].isnull()]
unique_publishers = remaining_publishers_df['publisher'].unique()

for publisher in unique_publishers:
    publisher_df = remaining_publishers_df[remaining_publishers_df['publisher'] == publisher]
    publisher_df.to_excel(os.path.join(output_folder, f'{publisher.replace("/", "_")}.xlsx'), index=False)