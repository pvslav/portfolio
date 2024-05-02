import os
import glob 
import json
import pandas as pd 
import xml.etree.ElementTree as ET 
from datetime import datetime 

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
        return dataframe  # Return an empty DataFrame in case of an error

    
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    dataframe.columns = ['Name', 'Weight', 'Height', 'City']  # Rename columns
    return dataframe

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

def extract():
    extracted_data = pd.DataFrame(columns=['Name', 'Weight', 'Height', 'City'])

    # процессируем все csv файлы
    for csvfile in glob.glob("*.csv"):
        extracted_data = pd.concat([extracted_data, extract_from_csv(csvfile)], ignore_index=True)

    # процессируем все json файлы
    for jsonfile in glob.glob("*.ndjson"):
        extracted_data = pd.concat([extracted_data, extract_from_json(jsonfile)], ignore_index=True)

    # процессируем все xml файлы
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat([extracted_data, extract_from_xml(xmlfile)], ignore_index=True)

    return extracted_data

def transform(data):
    '''Convert inches to meters and round off to two decimals
    1 inch is 0.0254 meters '''
    data['Height'] = data['Height'].apply(pd.to_numeric, errors='coerce') * 0.0254
    data['Height'] = data['Height'].round(2)

    '''Convert pounds to kilograms and round off to two decimals
    1 pound is 0.45359237 kilograms '''
    data['Weight'] = data['Weight'].apply(pd.to_numeric, errors='coerce') * 0.45359237
    data['Weight'] = data['Weight'].round(2)

    return data

def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file,"a") as f:
        f.write(timestamp + ',' + message + '\n')

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
