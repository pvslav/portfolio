import pandas as pd
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET
from datetime import date
import logging

url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'
url_rate = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
output_file_banks = 'bank_data.csv'
output_file_rates = 'currency_rates.csv'

def extract(url,max_rows=10):
    df = pd.DataFrame(columns=["Rank", "Bank_Name", "Total_assets"])
    count = 0

    try:
        html_page = requests.get(url).text
        data = BeautifulSoup(html_page, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return df

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        if count < max_rows:
            col = row.find_all('td')
            if len(col) != 0:
                rank = int(col[0].contents[0])
                bank_name = col[1].get_text(strip=True)
                total_assets = float(col[2].contents[0].replace(',', ''))
                data_dict = {"Rank": rank, "Bank_Name": bank_name, "Total_assets": total_assets}
                df = pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)
                count += 1
        else:
            break
    
    return df

def extract_rate(url_rate, output_file):
    # Get the XML data
    response = requests.get(url_rate)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        # Find the Cube nodes with currency and rate attributes
        cubes = root.findall(".//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@currency][@rate]")
        if cubes:
            data = []
            for cube in cubes:
                currency = cube.get('currency')
                if currency in ['USD', 'GBP']:
                    if currency == 'USD':
                        rate = round(1.0 / float(cube.get('rate')), 2)
                        currency = 'EUR'
                    else:
                        rate = round(float(cube.get('rate')), 2)
                    data.append({'Currency': currency, 'Rate': rate, 'Date': date.today()})

            # Create a DataFrame and save it to a CSV file
            df = pd.DataFrame(data)
            df.to_csv(output_file, index=False)

            print(f"Exchange rate data for EUR and GBP saved to file: {output_file}")
        else:
            print("Unable to find Cube nodes with currency and rate attributes in the XML file.")
    else:
        print(f"Error executing the request. Error code: {response.status_code}")

def transform(df, output_file_rates):
    # Read the CSV file with exchange rates and convert it to a dictionary
    exchange_rates = pd.read_csv(output_file_rates)
    exchange_rate_dict = dict(zip(exchange_rates['Currency'], exchange_rates['Rate']))
    
    # Rename the "Total_assets" column to "MC_USD_Billion"
    df = df.rename(columns={'Total_assets': 'MC_USD_Billion'})
    
    # Add the transformed total asset columns to the DataFrame
    df['MC_GBP_Billion'] = [round(x * exchange_rate_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [round(x * exchange_rate_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    
    return df

def main():
    try:
        # Configure logging
        logging.basicConfig(
            filename='app.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        bank_data = extract(url)
        bank_data.to_csv(output_file_banks, index=False)
        logging.info(f"Bank data saved to {output_file_banks}")

        extract_rate(url_rate, output_file_rates)
        logging.info(f"Currency rates saved to {output_file_rates}")
        
        transformed_df = transform(bank_data, output_file_rates)
        logging.info("Data transformation completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()