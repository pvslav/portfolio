# Airflow

In this project, we will create an automated pipeline that will daily extract the current exchange rates of major currencies from an online source, save the data to a CSV file, and upload that file to a designated GitHub repository. This will create a historical record of the exchange rates in the repository, with a new CSV file added each day.

To implement this pipeline, we will be using the Apache Airflow platform - a powerful tool for creating, scheduling, and monitoring complex data workflows.

Here is what the Airflow DAG for this pipeline will look like:

```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta, date
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import git

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_rates():
    # Get the XML data
    url_rate = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    response = requests.get(url_rate)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        # Find the Cube nodes with currency and rate attributes
        cubes = root.findall(".//{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube[@currency][@rate]")
        if cubes:
            data = []
            for cube in cubes:
                currency = cube.get('currency')
                rate = round(float(cube.get('rate')), 2)
                data.append([currency, rate])
            
            # Create a DataFrame and return it
            return pd.DataFrame(data, columns=['Currency', str(date.today())])
        else:
            print("Unable to find Cube nodes with currency and rate attributes in the XML file.")
            return None
    else:
        print(f"Error executing the request. Error code: {response.status_code}")
        return None

def upload_to_github(**context):
    # Get the DataFrame from the previous task
    exchange_rates = context['task_instance'].xcom_pull(task_ids='extract_rates')
    if exchange_rates is not None:
        # Save the DataFrame to a CSV file with the current date
        filename = f'exchange_rates_{str(date.today())}.csv'
        exchange_rates.to_csv(filename, index=False)
        
        # Initialize the Git repository
        repo = git.Repo('path/to/your/github/repository')
        repo.git.add(filename)
        repo.index.commit(f"Add {filename}")
        origin = repo.remote(name='origin')
        origin.push()
        
        print(f"File {filename} uploaded to GitHub.")

with DAG('currency_rates_to_github', default_args=default_args, schedule_interval='0 0 * * 0-6') as dag:
    extract_rates_task = PythonOperator(
        task_id='extract_rates',
        python_callable=extract_rates,
    )
    
    upload_to_github_task = PythonOperator(
        task_id='upload_to_github',
        python_callable=upload_to_github,
        provide_context=True,
    )
    
    extract_rates_task >> upload_to_github_task
```
