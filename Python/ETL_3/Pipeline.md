# Data Pipeline 

In our project, we will design a code that extracts the top 10 largest banks in the world by market capitalization in billion USD. This list will be processed and stored in GBP and EUR currencies, utilizing the latest available exchange rates online.

The resulting data will be saved in both CSV format for local storage and as a database table for future reference.

Our task is to develop an automated system for generating this information, enabling us to prepare quarterly reports seamlessly and efficiently. This system will streamline our reporting process, reducing manual errors and enhancing our operational efficiency.

## Step 1. Extract data

We write a function that will parse the data we need from a table on the Wikipedia page.

```python
url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'

def extract(url):
    df = pd.DataFrame(columns=["Rank", "Bank_Name", "Total_assets"])
    count = 0

    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        if count < 15:
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

df = extract(url)
print(df)
```
We'll get the following data from the page:

![extract_data](/Python/ETL_3/images/extract_data.png)

We also need to get the exchange rate for the current date. We retrieve exchange rates for USD and GBP. Then we convert USD to EUR and add a date column.

```python
def extract_rate(url, output_file):
    
    # Get the XML data
    response = requests.get(url)
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


extract_rate('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', 'currency_rates.csv')
```

![extract_rate](/Python/ETL_3/images/extract_rate.png)
