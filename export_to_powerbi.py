import sqlite3
import pandas as pd

# Connecting to the SQLite database
conn = sqlite3.connect(r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\export_import.db')

# Loading data from the table you want to import (for example, "Country")
table_name = 'Country'  # You can change this to 'CommodityFlow' or 'TradeDetails'
query = f"SELECT * FROM {table_name}"

# Executing the query and saving the result into a DataFrame
dataset = pd.read_sql_query(query, conn)

# Closing the database connection
conn.close()
