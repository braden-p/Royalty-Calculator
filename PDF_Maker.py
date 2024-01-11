import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def create_pdf(publisher_name, publisher_address, data):
    # Create PDF
    pdf_filename = f"{publisher_name.replace(' ', '_')}_statement.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

    # Header
    header = f"United States Mechanical Royalty Statement\n\nFrom:\nBasin Street Records\n\n{publisher_name}\n{publisher_address}\n\nJanuary 1, 2021 – December 31, 2022\n\nCurrent Period Royalties: {data['balance'].sum()}\n\n"
    
    # Table Data
    table_data = [
        ["Track Title", "Album Title", "UPC", "Product Type", "Rate Period", "Share", "Net Rate", "Net Units", "Amount Due"]
    ]

    for _, row in data.iterrows():
        table_data.append([
            row['track-title'],
            row['album-title'],
            row['upc'],
            row['product-type'],
            row['rate-period'],
            row['share'],
            row['net-rate'],
            row['net-units'],
            row['balance']
        ])

    # Subtotal Line
    subtotal_line = ["Subtotal:", "", "", "", "", "", "", "", data['balance'].sum()]
    table_data.append(subtotal_line)

    # Total Line
    total_line = ["Total:", "", "", "", "", "", "", "", data['balance'].sum()]
    table_data.append(total_line)

    # Build Table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build PDF
    content = [table]
    doc.build(content)

# Read royalty-run.xlsx
royalty_df = pd.read_excel('royalty-run.xlsx')

# Loop through unique publishers
for publisher_name, publisher_data in royalty_df.groupby('publisher'):
    publisher_address = "Your Publisher Address Here"  # Replace with actual publisher address
    create_pdf(publisher_name, publisher_address, publisher_data)