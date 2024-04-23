import requests
import pandas as pd
from sqlalchemy import create_engine, text, inspect,MetaData, Table, Column, String
from sqlalchemy.schema import CreateSchema

def extract()-> dict:
    API_URL = "http://universities.hipolabs.com/search?country=Germany"
    data = requests.get(API_URL).json()
    return data

def transform(data:dict) -> pd.DataFrame:
    df = pd.DataFrame(data)
    print(f"Total Number of universities from API {len(data)}")
    df = df[df["name"].str.contains("Berlin")]
    print(f"Number of universities in Berlin {len(df)}")
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(lambda x: x.rstrip('/'), l)) for l in df['web_pages']]
    pd.set_option('display.max_colwidth', None)
    return df

schema = "uni"
connectable = create_engine("postgresql+psycopg2://postgres@localhost/postgres")

with connectable.connect() as connection:
    if not inspect(connection).has_schema(schema):
        connection.execute(CreateSchema(schema))
        connection.commit()

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

# Extracting data and transforming it
data = extract()
df = transform(data)

# Loading data into the table
df.to_sql('universities', connectable, schema=schema, if_exists='replace', index=False)


