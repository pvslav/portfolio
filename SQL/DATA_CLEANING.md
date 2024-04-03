# DS jobs Information

Lets take a look at the first few rows to examine the data in its original form.

````sql
SELECT *
FROM science.ds_position
ORDER BY RANDOM()
LIMIT 10;
````

**Results:**

|index|job_title|salary_estimate|job_description|rating|company_name|location|headquarters|size|founded|type_ownership|industry|sector|revenue|competitors|
|-----|---------|---------------|---------------|------|------------|--------|------------|----|-------|--------------|--------|------|-------|-----------|
|660|Data Scientist|$105K-$167K (Glassdoor est.)|Location: Redmond, WA Client: Microsoft...|-1|Pactera Edge|Redmond, WA|-1|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|46|Senior Data Scientist|$75K-$131K (Glassdoor est.)|Analyze large data sets (we're..|4.8|Klaviyo 4.8|Boston, MA|Boston, MA|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|347|Data Engineer - Kafka|$122K-$146K (Glassdoor est.)|Western Digital® The next big thing in data...|3.5|Western Digital 3.5|San Jose, CA|San Jose, CA|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|150|Data Scientist|$90K-$109K (Glassdoor est.)|JOB SUMMARY Responsible for designing, analyzing...|2.9|SPECTRUM 2.9|Maryland Heights, MO|Stamford, CT|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|372|Data Scientist|$112K-$116K (Glassdoor est.)|Position is in support of the U.S. Army CCDC...|3.2|Perspecta 3.2|Adelphi, MD|Chantilly, VA|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|335|Data Scientist|$79K-$147K (Glassdoor est.)|One of the largest health insurers in the nation...|3.4|Solving IT International Inc 3.4|Chicago, IL|Chicago, IL|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|645|AI/ML - Machine Learning Scientist, Siri Understanding|$92K-$155K (Glassdoor est.)|Posted: May 2, 2020 Role Number:200018211...|4.1|Apple 4.1|Santa Clara, CA|Cupertino, CA|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|62|Data Scientist|$79K-$131K (Glassdoor est.)|Introduction Have you always wanted to run...|3.5|iRobot 3.5|Bedford, MA|Bedford, MA|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|487|Data Scientist, Applied Machine Learning - Bay Area|$95K-$119K (Glassdoor est.)|Passionate about precision medicine and advancing...|3.3|Tempus Labs 3.3|Redwood City, CA|Chicago, IL|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|
|9|Data Scientist|$137K-$171K (Glassdoor est.)|Ready to write the best chapter of your career? XSELL...|3.6|XSELL Technologies 3.6|Chicago, IL|Chicago, IL|1001 to 5000 employees|1993|Nonprofit Organization|Insurance Carriers|Insurance|Unknown / Non-Applicable|EmblemHealth, UnitedHealth Group, Aetna|



