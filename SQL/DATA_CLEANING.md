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
SELECT alary_estimate
FROM cleaned_jobs
LIMIT 5
````



