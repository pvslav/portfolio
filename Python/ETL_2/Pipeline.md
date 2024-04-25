# Data Pipeline 

In this project, we'll be extracting data from the different file's formats, transforming it, and loading it into PostgreSQL.
## Step 1. Conversion of JSON file to NDJSON.
Converting JSON format with an array to NDJSON (Newline-Delimited JSON) or JSON Lines format is quite common practice, especially when working with large data sets.NDJSON allows you to process data row by row, making operations such as filtering, transforming, and loading data easier and faster.
