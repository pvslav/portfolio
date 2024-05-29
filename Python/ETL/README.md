# ETL Pipeline 

In this project, we'll be extracting data from the API, transforming it, and loading it into PostgreSQL.

First, we import the required libraries:
- requests: to retrieve data from the API.
- pandas: to transform the data.
- sqlalchemy: to load the transformed data into PostgreSQL.

````python
import requests
import pandas as pd
from sqlalchemy import create_engine, text, inspect,MetaData, Table, Column, String
from sqlalchemy.schema import CreateSchema
````
Next we write a function to extract the data from the API. From this API we'll get the data about all the universities in Germany.

````python
def extract()-> dict:
    API_URL = "http://universities.hipolabs.com/search?country=Germany"
    data = requests.get(API_URL).json()
    return data
````
The following function displays the number of universities in Berlin, the name of each university and its website address.
````python
def transform(data:dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    print(f"Total Number of universities from API {len(data)}")
    df = df[df["name"].str.contains("Berlin")]
    print(f"Number of universities in Berlin {len(df)}")
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(lambda x: x.rstrip('/'), l)) for l in df['web_pages']]
    pd.set_option('display.max_colwidth', None)
    return df
````
![berlin_uni](/Python/ETL/images/berlin_uni.png)

Then we create a new schema. 

````python
schema = "uni"
connectable = create_engine("postgresql+psycopg2://postgres@localhost/postgres")

with connectable.connect() as connection:
    if not inspect(connection).has_schema(schema):
        connection.execute(CreateSchema(schema))
        connection.commit()
````
As the next step we create a university table in the “uni” schema. 

````python
metadata = MetaData(schema=schema)
universities_table = Table('universities', metadata,
                          Column('name', String),
                          Column('web_pages', String),
                          Column('alpha_two_code',String),
                          Column('state-province',String),
                          Column('domains',String),
                          Column('country',String)
                          )
metadata.create_all(connectable)
````
 The final step is the loading data in our table.
 
````python
# Extracting data and transforming it
data = extract()
df = transform(data)

# Loading data into the table
df.to_sql('universities', connectable, schema=schema, if_exists='replace', index=False)
````
This is what our table looks like after loading the data.

![uni_table](/Python/ETL/images/uni_table.png)

As you can see we need to make some more changes to our table.
First we will rename the "state-province" column.

````sql
ALTER TABLE uni.universities  RENAME COLUMN "state-province" TO state_province;
````

And finally, we will replace the null value with "Berlin" if there is this value in the name column.

````sql
UPDATE uni.universities 
SET state_province = 'Berlin'
WHERE name LIKE '%Berlin%' AND state_province IS NULL;
````
![final_uni](/Python/ETL/images/final_uni.png)

