import csv
import mysql.connector

# CSV access
csv_file = 'C:\\Users\\pc\\Desktop\\Data\\drugproducts1q_2024Updated05082024.csv'

# MySQL connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Fushiguro@11',
    'database': 'medication'
}

table_name = 'drugs'
column_name = 'drug_name'

# data from CSV
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

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {column_name} VARCHAR(255) NOT NULL
)
"""
cursor.execute(create_table_sql)

insert_sql = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"

for value in data_to_insert:
    cursor.execute(insert_sql, (value,))

conn.commit()
cursor.close()
conn.close()

print(f"Created table {table_name} (if it didn't exist) and inserted {len(data_to_insert)} rows into {column_name} column")