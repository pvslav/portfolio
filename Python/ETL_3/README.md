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
        if count < 10:
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

After executing this function, this is what our csv file will look like.

![extract_rate](/Python/ETL_3/images/extract_rate.png)

## Step 2. Transform data

This function renames column 'Total_assets' to 'MC_USD_Billion', adds two columns 'MC_GBP_Billion' and 'MC_EUR_Billion' and places in them the data from column 'MC_USD_Billion', converted according to the exchange rates that are in the csv file.

```python
def transform(df, csv_path):
    
    # Read the CSV file with exchange rates and convert it to a dictionary
    exchange_rates = pd.read_csv(csv_path)
    exchange_rate_dict = dict(zip(exchange_rates['Currency'], exchange_rates['Rate']))
    
    # Rename the "Total_assets" column to "MC_USD_Billion"
    df = df.rename(columns={'Total_assets': 'MC_USD_Billion'})
    
    # Add the transformed total asset columns to the DataFrame
    df['MC_GBP_Billion'] = [round(x * exchange_rate_dict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [round(x * exchange_rate_dict['EUR'], 2) for x in df['MC_USD_Billion']]
    
    return df

# Example usage
csv_path = 'currency_rates.csv'
transformed_df = transform(df, csv_path)
transformed_df
```
We'll get the following result

![transform](/Python/ETL_3/images/transform.png)


## Step 3. Create schema and table in the database

As the next step, we will write a function that will create a new schema and a table in the database.

```python
def create_schema_and_table():
    schema = "banks"
    connectable = create_engine("postgresql+psycopg2://postgres@localhost/postgres")

    with connectable.connect() as connection:
        if not Inspector(connection).has_schema(schema):
            connection.execute(CreateSchema(schema))
            connection.commit()

        # Create metadata for the table
        metadata = MetaData(schema=schema)

        # Define the table structure
        table = Table('largest_banks', metadata,
                     Column('rank', Integer),
                     Column('bank_name', String),
                     Column('mc_usd_billion', Float),
                     Column('mc_gbp_billion', Float),
                     Column('mc_eur_billion', Float))

        # Create the table
        metadata.create_all(connectable)

    print(f"Schema '{schema}' and table '{table.name}' created successfully.")

create_schema_and_table()
```

## Step 4. Loading ttansformed data to the database

This function will load the transformed data to the database.

```python
def load_to_database(df):
    schema = 'banks'
    connectable = create_engine("postgresql+psycopg2://postgres@localhost/postgres")
    
    # Loading data into the table
    df.to_sql('largest_banks', connectable, schema=schema, if_exists='replace', index=False)

load_to_database(transformed_df)
```

This is what our table looks like after loading the data.

![largest_banks](/Python/ETL_3/images/largest_banks.png)
