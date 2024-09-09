import sqlite3  # for working with the database
import os  # for checking file and directory existence
import pandas as pd  # for working with CSV files

# Define the path for saving the database
db_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\export_import.db'
report_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\DBTest.txt'

# Check if the directory where the database will be saved exists
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Connect to the database (if it doesn't exist, it will be created)
conn = sqlite3.connect(db_path)

# Create tables
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Country (
    id_primarykey INT PRIMARY KEY,
    country VARCHAR(100)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CommodityFlow (
    id_primarykey INT,
    year INT,
    commodity VARCHAR(255),
    flow VARCHAR(50),
    usd DECIMAL(15, 2),
    weight_kg DECIMAL(15, 3),
    quantity_name VARCHAR(100),
    quantity DECIMAL(15, 2),
    record VARCHAR(255),
    country VARCHAR(100),
    FOREIGN KEY (id_primarykey) REFERENCES Country(id_primarykey)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TradeDetails (
    id_primarykey INT,
    year INT,
    month INT,
    country VARCHAR(100),
    flow VARCHAR(50),
    partner2Desc VARCHAR(255),
    customscode VARCHAR(50),
    motcode VARCHAR(50),
    isgrosswgtestimated BOOLEAN,
    cifvalue DECIMAL(15, 2),
    fobvalue DECIMAL(15, 2),
    FOREIGN KEY (id_primarykey) REFERENCES Country(id_primarykey)
)
''')

# Save the changes
conn.commit()

# Function for loading CSV and inserting data into the tables
def load_csv_to_db_optimized(csv_path, table_name, conn, report):
    try:
        # Load the CSV file into a pandas DataFrame
        data = pd.read_csv(csv_path)
        total_rows = len(data)

        # Print column names and a few rows of the CSV for verification
        print(f"Columns in CSV {csv_path}: {list(data.columns)}")
        print(f"First few rows of {csv_path}:\n", data.head())

        # Insert all the data into the table at once
        data.to_sql(table_name, conn, if_exists='replace', index=False)

        # Update the report
        report[table_name] = {"total_rows_in_file": total_rows, "rows_inserted": total_rows}
    except Exception as e:
        print(f"Error loading data from {csv_path}: {e}")

# Updated paths to CSV files
csv_files = {
    'Country': r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\data\dataforDB\Country.csv',
    'CommodityFlow': r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\data\dataforDB\CommodityFlow.csv',
    'TradeDetails': r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\data\dataforDB\TradeDetails.csv'
}

# Initialize the report
report = {}

# Check for file existence and load data
for table_name, csv_path in csv_files.items():
    if not os.path.isfile(csv_path):
        print(f"File not found: {csv_path}")
        report[table_name] = {"total_rows_in_file": 0, "rows_inserted": 0}
    else:
        # Print column names and the first rows of the CSV
        data = pd.read_csv(csv_path)
        print(f"Columns in {csv_path}: {list(data.columns)}")
        print(f"First few rows of {csv_path}:\n{data.head()}")
        load_csv_to_db_optimized(csv_path, table_name, conn, report)

# Close the database connection
conn.close()

# Create a report in a txt file
with open(report_path, 'w') as f:
    f.write("Data Transfer Report:\n")
    for table, stats in report.items():
        f.write(f"Table '{table}': {stats['rows_inserted']} rows inserted out of {stats['total_rows_in_file']} total rows.\n")

print(f"\nDatabase 'export_import.db' has been created and data transfer report has been saved to 'DBTest.txt'.")
