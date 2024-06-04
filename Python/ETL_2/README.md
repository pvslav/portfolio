# Data Pipeline 

In this project, we'll be extracting data from the different file's formats, transforming it, and loading it into PostgreSQL.
## Step 1. Conversion of JSON file to NDJSON.
Converting JSON format with an array to NDJSON (Newline-Delimited JSON) or JSON Lines format is quite common practice, especially when working with large data sets. NDJSON allows you to process data row by row, making operations such as filtering, transforming, and loading data easier and faster. Many tools and technologies (eg Bash, Python, Spark) are better suited to working with row-by-row data.

Our json file looks like this

![json_file](/Python/ETL_2/images/json_file.png)


We'll write a function, that converts JSON to NDJSON.
```python
import os
import json
import glob

log_file = "log_file.txt" 
target_file = "transformed_data.csv" 

# Converting JSON to NDJSON
def convert_to_ndjson(input_file, output_file):
    with open(input_file, "r") as f:
        json_data = json.load(f)
    
    with open(output_file, "w") as f:
        for obj in json_data:
            json.dump(obj, f)
            f.write("\n")

# Find all files with the .json extension in the current directory
json_files = glob.glob("*.json")

# Converting the found JSON files to NDJSON
for json_file in json_files:
    output_file = os.path.splitext(json_file)[0] + ".ndjson"
    
    print(f"Converting {os.path.basename(json_file)} to NDJSON...")
    convert_to_ndjson(json_file, output_file)
    print("Conversion complete.")
```
```python
Converting file_3.json to NDJSON...
Conversion complete.
Converting file_4.json to NDJSON...
Conversion complete.
```
And this is what our converted file looks like

![ndjson_file](/Python/ETL_2/images/ndjson.png)

## Step 2. Extract data.
Now we need to extract data from different formats and put them into one file. First we will write three functions that will extract data from the appropriate formats. To avoid any issues when combining data into a single file in the future, we need to standardize the column formats in our files.

```python
def extract_from_csv(file_to_process):
    try:
        dataframe = pd.read_csv(file_to_process, header=0)  # Read CSV file, first row as headers
        
        if 'Unnamed: 0' in dataframe.columns:
            dataframe = dataframe.drop('Unnamed: 0', axis=1)
        
        known_cols = ['Name', 'Weight', 'Height', 'City']
        existing_cols = list(dataframe.columns)
        col_mapping = {col: known_col for known_col, col in zip(known_cols, existing_cols)}
        dataframe = dataframe.rename(columns=col_mapping)
        
        return dataframe
    except Exception as e:
        print(f"Error processing file {file_to_process}: {e}")
        return dataframe  # Return an empty DataFrame in case of an err
```
This function extracts data from json files.

```python
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    dataframe.columns = ['Name', 'Weight', 'Height', 'City']  # Rename columns
    return dataframe
```
This function extracts data from xml files.

```python
def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=["Name", "Weight", "Height", "City"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("Name").text
        height = float(person.find("Height_in").text)
        weight = float(person.find("Weight_lbs").text)
        city = person.find("City").text
        dataframe = pd.concat([dataframe, pd.DataFrame([{"Name": name, "Weight": weight, "Height": height, "City": city}])], ignore_index=True)
    return dataframe
```
Finally we collect data from all the files.

```python
def extract():
    extracted_data = pd.DataFrame(columns=['Name', 'Weight', 'Height', 'City'])

    # process all csv files
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)

    # process all json files
    for jsonfile in glob.glob("*.ndjson"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)

    # process all xml files
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)

    return extracted_data
```
## Step 3. Transform data.

If we look at the column names in the files, we will see that in the height column the data is given in inches, and in the weight column the data is in pounds. We need to convert the data in these columns: inches to meters, pounds to kilograms. We will do this in the transform function.

![convet_measures](/Python/ETL_2/images/convert_measures.png)

```python
def transform(data):
    '''Convert inches to meters and round off to two decimals
    1 inch is 0.0254 meters '''
    try:
        data['Height'] = data['Height'].astype(float) * 0.0254
        data['Height'] = data['Height'].round(2)
    except ValueError:
        print("Error: non-numeric values found in Height column.")

    '''Convert pounds to kilograms and round off to two decimals
    1 pound is 0.45359237 kilograms '''
    try:
        data['Weight'] = data['Weight'].astype(float) * 0.45359237
        data['Weight'] = data['Weight'].round(2)
    except ValueError:
        print("Error: non-numeric values found in Weight column.")

    return data
```
## Step 4. Loading and Logging.

We need to load the transformed data to a CSV file that we can use to load to a database as per requirement. We need a function load_data() that accepts the transformed data as a dataframe and the target_file path. We also need to use the to_csv attribute of the dataframe in the function. 

```python
def load_data(target_file, transformed_data): 
    transformed_data.to_csv(target_file,index=False) 
```
Finally, we need to implement the logging operation to record the progress of the different operations.

```python
def log_progress(message): 
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ',' + message + '\n') 
```
## Step 5. Testing ETL process.

Now, we will test the functions we have developed so far and log our progress along the way. 

```python
# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract() 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_data(target_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 
 
# Log the completion of the ETL process 
log_progress("ETL Job Ended")  
```
## Step 6. Loading data to Postgres.

```python
# Create an engine object to connect to the database
engine = create_engine("postgresql+psycopg2://postgres@localhost/postgres")

metadata = MetaData(schema="uni")
names_table = Table('names', metadata,
                    Column('Name', String),
                    Column('Weight', Float),
                    Column('Height', Float),
                    Column('City', String),
                    )

try:
    metadata.create_all(engine)
    print("Table 'names' successfully created in schema 'uni'.")
except Exception as e:
    print(f"Error creating table 'names': {e}")

# Read data from CSV file into DataFrame
data = pd.read_csv('transformed_data.csv')

try:
    data.to_sql('names', engine, schema='uni', if_exists='append', index=False)
    print("Data successfully loaded into table 'names' in schema 'uni'.")
except Exception as e:
    print(f"Error loading data into table 'names': {e}")
```

This is what our data looks like in the database.

![table_names](/Python/ETL_2/images/table_names.png)

