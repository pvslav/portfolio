# DS jobs Information

Lets take a look at the few random rows to examine the data in its original form.

````sql
SELECT *
FROM science.ds_position
ORDER BY RANDOM()
LIMIT 10;
````

**Results:**

|index|job_title|salary_estimate|job_description|rating|company_name|location|headquarters|size|founded|type_ownership|industry|sector|revenue|competitors|
|-----|---------|---------------|---------------|------|------------|--------|------------|----|-------|--------------|--------|------|-------|-----------|
|660|Data Scientist|$105K-$167K (Glassdoor est.)|Location: Redmond, WA Client: Microsoft...|-1|Pactera Edge|Redmond, WA|-1|-1|-1|-1|-1|-1|-1|-1|
|46|Senior Data Scientist|$75K-$131K (Glassdoor est.)|Analyze large data sets (we're..|4.8|Klaviyo 4.8|Boston, MA|Boston, MA|201 to 500 employees|2012|Company - Private|Computer Hardware & Software|Information Technology|Unknown / Non-Applicable|-1|
|347|Data Engineer - Kafka|$122K-$146K (Glassdoor est.)|Western Digital® The next big thing in data...|3.5|Western Digital 3.5|San Jose, CA|San Jose, CA|10000+ employees|1970|Company - Public|Computer Hardware & Software|Information Technology|$10+ billion (USD)|Seagate Technology, Toshiba|
|150|Data Scientist|$90K-$109K (Glassdoor est.)|JOB SUMMARY Responsible for designing, analyzing...|2.9|SPECTRUM 2.9|Maryland Heights, MO|Stamford, CT|10000+ employees|2016|Subsidiary or Business Segment|Cable, Internet & Telephone Providers|Telecommunications|$10+ billion (USD)|-1|
|372|Data Scientist|$112K-$116K (Glassdoor est.)|Position is in support of the U.S. Army CCDC...|3.2|Perspecta 3.2|Adelphi, MD|Chantilly, VA|10000+ employees|2018|Company - Public|Aerospace & Defense|Aerospace & Defense|Unknown / Non-Applicable|-1|
|335|Data Scientist|$79K-$147K (Glassdoor est.)|One of the largest health insurers in the nation...|3.4|Solving IT International Inc 3.4|Chicago, IL|Chicago, IL|501 to 1000 employees|-1|Company - Private|-1|-1|Unknown / Non-Applicable|-1|
|645|AI/ML - Machine Learning Scientist, Siri Understanding|$92K-$155K (Glassdoor est.)|Posted: May 2, 2020 Role Number:200018211...|4.1|Apple 4.1|Santa Clara, CA|Cupertino, CA|10000+ employees|1976|Company - Public|Computer Hardware & Software|Information Technology|$10+ billion (USD)|Google, Microsoft, Samsung Electronics|
|62|Data Scientist|$79K-$131K (Glassdoor est.)|Introduction Have you always wanted to run...|3.5|iRobot 3.5|Bedford, MA|Bedford, MA|1001 to 5000 employees|1990|Company - Public|Consumer Electronics & Appliances Stores|Retail|$1 to $2 billion (USD)|-1|
|487|Data Scientist, Applied Machine Learning - Bay Area|$95K-$119K (Glassdoor est.)|Passionate about precision medicine and advancing...|3.3|Tempus Labs 3.3|Redwood City, CA|Chicago, IL|501 to 1000 employees|2015|Company - Private|Biotech & Pharmaceuticals|Biotech & Pharmaceuticals|Unknown / Non-Applicable|-1|
|9|Data Scientist|$137K-$171K (Glassdoor est.)|Ready to write the best chapter of your career? XSELL...|3.6|XSELL Technologies 3.6|Chicago, IL|Chicago, IL|51 to 200 employees|2014|Company - Private|Enterprise Software & Network Solutions|Information Technology|Unknown / Non-Applicable|-1|

## Step 1. Create a new table to work with
Lets create a temp table where we can manipulate and restructure the data without altering the original.

````sql
DROP TABLE IF EXISTS cleaned_jobs;
CREATE TABLE cleaned_jobs AS 
SELECT *
FROM ds_position;
````
## Step 2. Examine the table structure
As a next step we'll examine the structure of our table to retrieve information about the columns in the table.

````sql
SELECT 
  column_name, 
  data_type, 
  character_maximum_length, 
  is_nullable, 
  column_default 
FROM 
  information_schema.columns 
WHERE 
  table_name = 'cleaned_jobs';
````
![table_structure](/SQL/images/table_structure.png)

## Step 3. Extract unnecessary characters
For our next step, we will be extracting the ‘(Glassdoor est.)” values from the column "salary_estimate" keeping just the figures.

````sql
-- examine salary_estimate column
SELECT salary_estimate
FROM cleaned_jobs
LIMIT 5
````
![salary_column](/SQL/images/salary_column.png)

````sql
UPDATE cleaned_jobs 
SET salary_estimate = REGEXP_REPLACE(salary_estimate , '(\$[0-9]+K-\$[0-9]+K).*', '\1')
````
![salary_cleaned](/SQL/images/salary_cleaned.png)

## Step 4. Clean the company_name column
As  we can  seen,  the column "company_name" contains some unnecessary characters that needs to be removed. We can do this using the following query.
````sql
UPDATE cleaned_jobs
SET company_name = 
    CASE 
        WHEN POSITION(E'\n' IN company_name) > 0 
        THEN SUBSTRING(company_name FROM 1 FOR POSITION(E'\n' IN company_name) - 1) 
        ELSE company_name 
    END;
````
![new_colunm_name](/SQL/images/new_column_name.png)

## Step 5. Fix the size column
To make the column "size" look more attractive, we will replace "to" with "-".

````sql
UPDATE cleaned_jobs
SET size = 
    CASE
        WHEN size = '-1' THEN NULL
        ELSE REPLACE(size, ' to ', '-')
    END;
````
![size_column](/SQL/images/size_column.png)

## Step 6. Replace the value "-1"
As you can see in the origin table above, some colunm have the value "-1". We will replace this value with NULL.


````sql
DO
$$
DECLARE
    v_table_name VARCHAR(255) := 'cleaned_jobs';
    v_column_name VARCHAR(255);
    v_sql_query VARCHAR(1000);
BEGIN
    -- Create a cursor to iterate through all columns in the table
    FOR v_column_name IN
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = v_table_name
    LOOP
        -- Generate a dynamic SQL query to update values
        v_sql_query := 'UPDATE ' || quote_ident(v_table_name) || ' SET ' || quote_ident(v_column_name) || ' = NULL WHERE ' || quote_ident(v_column_name) || ' = ''-1''';
        -- Execute a dynamic SQL query
        EXECUTE v_sql_query;
    END LOOP;
END;
$$;
````
![replace_values](/SQL/images/replace_values.png)


## Step 7. Clean the type_ownership column. 
This column contains data we need to standardize, i.e changing the “Company — Private” and “Company — Public” values for easier reading.

````sql
UPDATE cleaned_jobs
SET type_ownership = 
    CASE 
        WHEN type_ownership = 'Company - Private' THEN 'Private Company'
        WHEN type_ownership = 'Company - Public' THEN 'Public Company'
        ELSE type_ownership -- Keeps other values unchanged
    END;
````
````sql
SELECT type_ownership
FROM cleaned_jobs
GROUP BY type_ownership
````
![ownership](/SQL/images/ownership.png)
