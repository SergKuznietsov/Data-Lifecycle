import logging
import pandas as pd
import glob
import os
import xml.etree.ElementTree as ET
import time

# Logging configuration
logging.basicConfig(
    filename=r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\process_log.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Paths to directories
raw_data_csv_path = r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\raw_data\csv"
raw_data_xml_path = r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\raw_data\xml"
cleaned_data_path = r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data"
report_path = r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\DataFrame.txt"

logging.info("Data processing started")

try:
    # Function to process TradeData_*.csv files
    def process_trade_data():
        start_time = time.time()
        logging.info("Processing TradeData_*.csv files")
        trade_files = glob.glob(os.path.join(raw_data_csv_path, "TradeData_*.csv"))
        trade_df_list = []
        initial_row_count = 0
        for file in trade_files:
            logging.info(f"Processing file: {file}")
            df = pd.read_csv(file)
            initial_row_count += df.shape[0]
            trade_df_list.append(df)
        trade_combined_df = pd.concat(trade_df_list, ignore_index=True)
        trade_combined_df.to_csv(os.path.join(cleaned_data_path, "DataFrameTrade.csv"), index=False)
        logging.info("Saved DataFrameTrade.csv")
        end_time = time.time()
        logging.info(f"Time taken to process TradeData_*.csv: {end_time - start_time} seconds")
        return initial_row_count, trade_combined_df.shape[0]

    # Function to process UNdata_Export_*.csv and UNdata_Export_*.xml files
    def process_un_data_export():
        start_time = time.time()
        logging.info("Processing UNdata_Export_*.csv files")
        un_data_files_csv = glob.glob(os.path.join(raw_data_csv_path, "UNdata_Export_*.csv"))
        un_data_df_list = []
        initial_row_count_csv = 0
        for file in un_data_files_csv:
            logging.info(f"Processing file: {file}")
            df = pd.read_csv(file)
            initial_row_count_csv += df.shape[0]
            un_data_df_list.append(df)
        un_data_combined_df = pd.concat(un_data_df_list, ignore_index=True)

        logging.info("Processing UNdata_Export_*.xml files")
        un_data_files_xml = glob.glob(os.path.join(raw_data_xml_path, "UNdata_Export_*.xml"))
        initial_row_count_xml = 0
        for file in un_data_files_xml:
            logging.info(f"Processing file: {file}")
            tree = ET.parse(file)
            root = tree.getroot()
            all_records = []
            for child in root:
                record = {}
                for element in child:
                    record[element.tag] = element.text
                all_records.append(record)
            xml_df = pd.DataFrame(all_records)
            initial_row_count_xml += xml_df.shape[0]
            un_data_combined_df = pd.concat([un_data_combined_df, xml_df], ignore_index=True)

        final_row_count = un_data_combined_df.shape[0]
        if final_row_count > 0:
            un_data_combined_df.to_csv(os.path.join(cleaned_data_path, "DataFrameUNdataExport.csv"), index=False)
            logging.info("Saved DataFrameUNdataExport.csv")
        else:
            logging.info("No data to save for DataFrameUNdataExport.csv")

        end_time = time.time()
        logging.info(f"Time taken to process UNdata_Export_*.csv and UNdata_Export_*.xml: {end_time - start_time} seconds")
        return initial_row_count_csv + initial_row_count_xml, final_row_count

    # Function to remove empty files
    def remove_empty_files(file_path):
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            logging.info(f"Removing empty file: {file_path}")
            os.remove(file_path)

    # Process the data and get row counts
    trade_initial_count, trade_final_count = process_trade_data()
    un_data_initial_count, un_data_final_count = process_un_data_export()

    # Remove the empty DataFrameUNdataExport.csv file if it exists
    remove_empty_files(os.path.join(cleaned_data_path, "DataFrameUNdataExport.csv"))

    # Create report with detailed information
    report_content = (
        f"Data Processing Report:\n"
        f"File DataFrameTrade.csv:\n"
        f" - Initial row count: {trade_initial_count}\n"
        f" - Final row count: {trade_final_count}\n\n"
        f"File DataFrameUNdataExport.csv:\n"
        f" - Initial row count: {un_data_initial_count}\n"
        f" - Final row count: {un_data_final_count}\n"
    )

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_content)

    logging.info("Data processing completed successfully")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
    print(f"An error occurred: {str(e)}")
