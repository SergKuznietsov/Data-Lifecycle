import pandas as pd

# File paths (replace the paths with actual ones)
cleaned_data_file = r'path_to_your_files\Clean_data.csv'
vehicles_file = r'path_to_your_files\vehicles.csv'
locations_file = r'path_to_your_files\locations.csv'
utilities_file = r'path_to_your_files\utilities.csv'
foreign_keys_file = r'path_to_your_files\foreign_keys.csv'

# Loading CSV files
clean_data = pd.read_csv(cleaned_data_file)
vehicles_data = pd.read_csv(vehicles_file)
locations_data = pd.read_csv(locations_file)
utilities_data = pd.read_csv(utilities_file)
foreign_keys_data = pd.read_csv(foreign_keys_file)

# Getting unique values from the 'DOL_Vehicle_ID' column
clean_unique_ids = set(clean_data['DOL_Vehicle_ID'].unique())
vehicles_unique_ids = set(vehicles_data['DOL_Vehicle_ID'].unique())
locations_unique_ids = set(locations_data['DOL_Vehicle_ID'].unique())
utilities_unique_ids = set(utilities_data['DOL_Vehicle_ID'].unique())
foreign_keys_unique_ids = set(foreign_keys_data['DOL_Vehicle_ID'].unique())

# Comparing unique values between Clean_data and other files
vehicles_diff = len(clean_unique_ids - vehicles_unique_ids)
locations_diff = len(clean_unique_ids - locations_unique_ids)
utilities_diff = len(clean_unique_ids - utilities_unique_ids)
foreign_keys_diff = len(clean_unique_ids - foreign_keys_unique_ids)

# Creating a report
report = f"""
Comparison of unique 'DOL_Vehicle_ID' values between Clean_data.csv and other files:

vehicles.csv:
  Unique values in vehicles.csv: {len(vehicles_unique_ids)}
  Difference from Clean_data.csv: {vehicles_diff} values

locations.csv:
  Unique values in locations.csv: {len(locations_unique_ids)}
  Difference from Clean_data.csv: {locations_diff} values

utilities.csv:
  Unique values in utilities.csv: {len(utilities_unique_ids)}
  Difference from Clean_data.csv: {utilities_diff} values

foreign_keys.csv:
  Unique values in foreign_keys.csv: {len(foreign_keys_unique_ids)}
  Difference from Clean_data.csv: {foreign_keys_diff} values
"""

# Writing the report to a text file
report_file = r'path_to_your_files\comparison_report.txt'
with open(report_file, 'w') as f:
    f.write(report)

print("Comparison report generated and saved.")
