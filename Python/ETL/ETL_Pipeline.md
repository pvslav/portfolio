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

````python
def load(df: pd.DataFrame) -> None:
    """Loads data into a PostgreSQL database."""
    # Укажите параметры подключения к вашей базе данных PostgreSQL
    db_username = 'slava'
    db_password = '1289'
    db_host = 'localhost'  # или IP-адрес сервера PostgreSQL
    db_port = '5432'  # порт по умолчанию для PostgreSQL
    db_name = 'postgres'

    # Формируем строку подключения к PostgreSQL
    db_string = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Создаем движок базы данных SQLAlchemy
    db_engine = create_engine(db_string)

    # Загружаем данные в PostgreSQL
    df.to_sql('list_uni', db_engine, if_exists='replace', index=False)

# Вызываем функцию extract() для извлечения данных
data = extract()

# Вызываем функцию transform() для преобразования данных в DataFrame
df = transform(data)

# Вызываем функцию load() для загрузки данных в базу данных
load(df)
````
