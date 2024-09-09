import pandas as pd
import os
import xml.etree.ElementTree as ET

# Paths to the directories containing the files
csv_dir = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\raw_data\csv'
xlsx_dir = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\raw_data\xlsx'
xml_dir = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\raw_data\xml'

# Path to the output report file
report_file_path = r'D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\data_check_report.txt'

# Initialize counters and detailed logs for statistics
total_files = 0
checked_files = 0
skipped_files = 0

csv_stats = {"duplicates": 0, "missing_values": 0, "invalid_formats": 0, "missing_detail": {}, "format_detail": {}}
xlsx_stats = {"duplicates": 0, "missing_values": 0, "invalid_formats": 0, "missing_detail": {}, "format_detail": {}}
xml_stats = {"record_count": 0, "record_detail": {}}

def check_csv_file(file_path):
    global checked_files, skipped_files, csv_stats
    try:
        df = pd.read_csv(file_path, encoding='latin1')
        checked_files += 1

        # Check for missing values
        missing_values_count = df.isnull().sum()
        if missing_values_count.sum() > 0:
            csv_stats["missing_values"] += missing_values_count.sum()
            csv_stats["missing_detail"][file_path] = missing_values_count[missing_values_count > 0].to_dict()

        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if (duplicate_count > 0):
            csv_stats["duplicates"] += duplicate_count
            csv_stats["format_detail"][file_path] = {"duplicates": duplicate_count}
            
    except Exception as e:
        skipped_files += 1
        print(f"Error processing {file_path}: {str(e)}")

def check_xlsx_file(file_path):
    global checked_files, skipped_files, xlsx_stats
    try:
        df = pd.read_excel(file_path)
        checked_files += 1

        # Check for missing values
        missing_values_count = df.isnull().sum()
        if missing_values_count.sum() > 0:
            xlsx_stats["missing_values"] += missing_values_count.sum()
            xlsx_stats["missing_detail"][file_path] = missing_values_count[missing_values_count > 0].to_dict()

        # Check for duplicates
        duplicate_count = df.duplicated().sum()
        if (duplicate_count > 0):
            xlsx_stats["duplicates"] += duplicate_count
            xlsx_stats["format_detail"][file_path] = {"duplicates": duplicate_count}
            
    except Exception as e:
        skipped_files += 1
        print(f"Error processing {file_path}: {str(e)}")

def count_xml_records(file_path):
    global checked_files, skipped_files, xml_stats
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Count the number of records (assuming each data record is represented by an element)
        record_count = len(root)
        xml_stats["record_count"] += record_count
        xml_stats["record_detail"][file_path] = {"record_count": record_count}
        checked_files += 1
        
    except Exception as e:
        skipped_files += 1
        print(f"Error processing {file_path}: {str(e)}")

# Processing each directory
for file_name in os.listdir(csv_dir):
    if file_name.endswith('.csv'):
        check_csv_file(os.path.join(csv_dir, file_name))

for file_name in os.listdir(xlsx_dir):
    if file_name.endswith('.xlsx'):
        check_xlsx_file(os.path.join(xlsx_dir, file_name))

for file_name in os.listdir(xml_dir):
    if file_name.endswith('.xml'):
        count_xml_records(os.path.join(xml_dir, file_name))

# Writing the report to a file
with open(report_file_path, 'w') as report_file:
    report_file.write(f"Total files: {total_files}\n")
    report_file.write(f"Checked files: {checked_files}\n")
    report_file.write(f"Skipped files: {skipped_files}\n")
    report_file.write("\nCSV Stats:\n")
    report_file.write(f"Missing values: {csv_stats['missing_values']}\n")
    report_file.write(f"Duplicates: {csv_stats['duplicates']}\n")
    report_file.write("\nXLSX Stats:\n")
    report_file.write(f"Missing values: {xlsx_stats['missing_values']}\n")
    report_file.write(f"Duplicates: {xlsx_stats['duplicates']}\n")
    report_file.write("\nXML Stats:\n")
    report_file.write(f"Total Records: {xml_stats['record_count']}\n")
    for file_path, detail in xml_stats["record_detail"].items():
        report_file.write(f"{file_path}: {detail['record_count']} records\n")
