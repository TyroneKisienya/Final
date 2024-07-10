import csv
import mysql.connector

# CSV file path - update this to the correct path
csv_file = 'C:\\Users\\pc\\Desktop\\Data\\drugproducts1q_2024Updated05082024.csv'  # Replace with your actual file path

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Fushiguro@11',
    'database': 'medication'
}

# Table and column names in MySQL
table_name = 'drugs'
column_name = 'drug_name'

# Read data from CSV
data_to_insert = []
with open(csv_file, 'r') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Read the header row
    fda_product_name_index = headers.index('Reactivation Date')
    
    for row in csv_reader:
        if len(row) > fda_product_name_index:
            drug_name = row[fda_product_name_index].strip()
            if drug_name:  # Only add non-empty names
                data_to_insert.append(drug_name)

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create table if not exists
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {column_name} VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_sql)

# Prepare SQL query for insertion
insert_sql = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"

# Execute insert for each value
for value in data_to_insert:
    cursor.execute(insert_sql, (value,))

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print(f"Created table {table_name} (if it didn't exist) and inserted {len(data_to_insert)} rows into {column_name} column")