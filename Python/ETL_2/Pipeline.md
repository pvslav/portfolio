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
    dataframe = pd.read_csv(file_to_process)
    dataframe.columns = ['Name', 'Weight', 'Height', 'City']  # Rename columns
    return dataframe
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
