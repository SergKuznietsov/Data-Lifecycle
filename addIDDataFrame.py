import pandas as pd

# Paths to the files
id_primarykey_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data\id_primarykey.csv'
trade_file_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data\DataFrameTrade.csv'
export_file_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data\DataFrameUNdataExport.csv'
contraceptive_file_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data\ContraceptivePrevalenceMethod.xlsx'

# 1. Reading the id_primarykey.csv file with specified encoding
id_df = pd.read_csv(id_primarykey_path, encoding='ISO-8859-1')  # Try 'windows-1252' or 'utf-8' if needed

# Checking for the existence of required columns
required_columns = ['Country Name', 'id_primarykey']
if not all(col in id_df.columns for col in required_columns):
    raise ValueError(f"The file id_primarykey.csv must contain the columns: {required_columns}")

# 2. Reading DataFrameTrade_cleaned.csv and DataFrameUNdataExport.csv files with specified encoding
trade_df = pd.read_csv(trade_file_path, encoding='ISO-8859-1')
export_df = pd.read_csv(export_file_path, encoding='ISO-8859-1')

# 3. Merging with DataFrameTrade_cleaned.csv based on the 'reporterISO' column
trade_df = trade_df.merge(id_df[['Country Name', 'id_primarykey']], how='left', left_on='reporterISO', right_on='Country Name')

# Checking for missing id_primarykey values in DataFrameTrade_cleaned.csv
missing_trade_ids = trade_df[trade_df['id_primarykey'].isna()]
if not missing_trade_ids.empty:
    print("Warning: Missing id_primarykey for the following records in DataFrameTrade_cleaned.csv:")
    print(missing_trade_ids[['reporterISO']])

# 4. Merging with DataFrameUNdataExport.csv based on the 'Country or Area' column
export_df = export_df.merge(id_df[['Country Name', 'id_primarykey']], how='left', left_on='Country or Area', right_on='Country Name')

# Checking for missing id_primarykey values in DataFrameUNdataExport.csv
missing_export_ids = export_df[export_df['id_primarykey'].isna()]
if not missing_export_ids.empty:
    print("Warning: Missing id_primarykey for the following records in DataFrameUNdataExport.csv:")
    print(missing_export_ids[['Country or Area']])

# 5. Reading and updating the Excel file ContraceptivePrevalenceMethod.xlsx
contraceptive_df = pd.read_excel(contraceptive_file_path)

# Merging with contraceptive_df based on the 'Country Name' column
contraceptive_df = contraceptive_df.merge(id_df[['Country Name', 'id_primarykey']], how='left', left_on='Country Name', right_on='Country Name')

# Checking for missing id_primarykey values in ContraceptivePrevalenceMethod.xlsx
missing_contraceptive_ids = contraceptive_df[contraceptive_df['id_primarykey'].isna()]
if not missing_contraceptive_ids.empty:
    print("Warning: Missing id_primarykey for the following records in ContraceptivePrevalenceMethod.xlsx:")
    print(missing_contraceptive_ids[['Country Name']])

# 6. Saving the updated files
trade_df.to_csv(trade_file_path, index=False)
export_df.to_csv(export_file_path, index=False)
contraceptive_df.to_excel(contraceptive_file_path, index=False)
