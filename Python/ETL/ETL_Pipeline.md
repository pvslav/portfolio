# ETL Pipeline 

In this project, we'll be extracting data from the API, transforming it, and loading it into PostgreSQL.

First, we import the required libraries:
- requests: to retrieve data from the API.
- pandas: to transform the data.
- sqlalchemy: to load the transformed data into PostgreSQL.

````python
import requests
import pandas as pd
from sqlalchemy import create_engine
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
    return df[["name", "web_pages"]]
````
![berlin_uni](/Python/ETL/images/berlin_uni.png)
