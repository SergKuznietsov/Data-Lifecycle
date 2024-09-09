from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import csv
import os
import time

# Setup the web driver using Service class (replace with your correct path)
driver_path = r'D:\download\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
driver.get(url)

# Allow some time for the page to load completely
time.sleep(5)

# Get page source after rendering JavaScript
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Close the browser
driver.quit()

# Directory where you want to save the CSV file
save_directory = r"D:\Finance_success\DataAnalytics\Portfolio\Python\2.Data Lifecycle\cleaned_data"
os.makedirs(save_directory, exist_ok=True)

# File path where the CSV will be saved
csv_file_path = os.path.join(save_directory, 'iso_3166_country_codes_extended.csv')

# Locate all tables on the page
tables = soup.find_all('table')

# Check if any tables were found
if len(tables) == 0:
    print("No tables found on the page.")
else:
    print(f"Found {len(tables)} tables. Using the first one.")

    # Use the first table found
    table = tables[0]

    # Extract table rows
    rows = table.find_all('tr')

    # Prepare CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header row based on the image provided
        csv_writer.writerow([
            'ISO 3166 Name', 
            'World Factbook Official Name', 
            'Sovereignty', 
            'A-2 Code', 
            'A-3 Code', 
            'Numeric Code', 
            'Subdivision Codes Link', 
            'TLD'
        ])

        # Iterate over the rows and extract the relevant data
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            
            if len(columns) >= 8:  # Ensure we have enough columns
                iso_3166_name = columns[0].text.strip()
                world_factbook_name = columns[1].text.strip()
                sovereignty = columns[2].text.strip()
                alpha_2 = columns[3].text.strip()
                alpha_3 = columns[4].text.strip()
                numeric_code = columns[5].text.strip()
                subdivision_link = columns[6].text.strip()  # Subdivision codes link
                tld = columns[7].text.strip()  # TLD
                
                # Write the row to the CSV file
                csv_writer.writerow([
                    iso_3166_name, 
                    world_factbook_name, 
                    sovereignty, 
                    alpha_2, 
                    alpha_3, 
                    numeric_code, 
                    subdivision_link, 
                    tld
                ])

    print(f"ISO 3166 country codes with additional data saved to {csv_file_path}")

# Adding a delay to avoid being rate-limited or blocked
time.sleep(2)
