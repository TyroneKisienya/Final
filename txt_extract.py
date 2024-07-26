import csv
import os

# CSV access
csv_file = 'C:\\Users\\pc\\Desktop\\Data\\drugproducts1q_2024Updated05082024.csv'

# Output file name
output_file = 'extracted_drug_names.txt'

# data from CSV
data_to_extract = []
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Read the header row
    fda_product_name_index = headers.index('Reactivation Date')
    
    for row in csv_reader:
        if len(row) > fda_product_name_index:
            drug_name = row[fda_product_name_index].strip()
            if drug_name:  # Only add non-empty names
                data_to_extract.append(drug_name)

# Write extracted data to text file
with open(output_file, 'w') as file:
    for drug_name in data_to_extract:
        file.write(drug_name + '\n')

print(f"Extracted {len(data_to_extract)} drug names and saved them to {output_file}")