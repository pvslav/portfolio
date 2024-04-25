# Data Pipeline 

In this project, we'll be extracting data from the different file's formats, transforming it, and loading it into PostgreSQL.
## Step 1. Conversion of JSON file to NDJSON.
Converting JSON format with an array to NDJSON (Newline-Delimited JSON) or JSON Lines format is quite common practice, especially when working with large data sets. NDJSON allows you to process data row by row, making operations such as filtering, transforming, and loading data easier and faster. Many tools and technologies (eg Bash, Python, Spark) are better suited to working with row-by-row data.

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
```
    print("Conversion complete.")
