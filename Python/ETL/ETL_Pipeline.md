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
