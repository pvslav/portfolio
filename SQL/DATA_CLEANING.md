# DS jobs Information

Lets take a look at the first few rows to examine the data in its original form.

````sql
SELECT 
	*
FROM science.ds_position 
LIMIT 10;
````

**Results:**

index|job_title                               |salary_estimate             |job_description                                                                                                                                                                                                                                                |rating|company_name          |location         |headquarters          |size                   |founded|type_ownership         |industry                                |sector                   |revenue                   |competitors                                           |
-----+----------------------------------------+----------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------+----------------------+-----------------+----------------------+-----------------------+-------+-----------------------+----------------------------------------+-------------------------+--------------------------+------------------------------------------------------+
    0|Sr Data Scientist                       |$137K-$171K (Glassdoor est.)|Description¶¶The Senior Data Scientist is responsible for defining, building, and improving statistical models to improve business processes and outcomes in one or more healthcare domains such as Clinical, Enrollment, Claims, and Finance. As part of the b|   3.1|Healthfirst¶3.1       |New York, NY     |New York, NY          |1001 to 5000 employees |   1993|Nonprofit Organization |Insurance Carriers                      |Insurance                |Unknown / Non-Applicable  |EmblemHealth, UnitedHealth Group, Aetna               |
    1|Data Scientist                          |$137K-$171K (Glassdoor est.)|Secure our Nation, Ignite your Future¶¶Join the top Information Technology and Analytic professionals in the industry to make invaluable contributions to our national security on a daily basis. In this innovative, self-contained, Big Data environment, the|   4.2|ManTech¶4.2           |Chantilly, VA    |Herndon, VA           |5001 to 10000 employees|   1968|Company - Public       |Research & Development                  |Business Services        |$1 to $2 billion (USD)    |-1                                                    |
    2|Data Scientist                          |$137K-$171K (Glassdoor est.)|Overview¶¶¶Analysis Group is one of the largest international economics consulting firms, with more than 1,000 professionals across 14 offices in North America, Europe, and Asia. Since 1981, we have provided expertise in economics, finance, health care an|   3.8|Analysis Group¶3.8    |Boston, MA       |Boston, MA            |1001 to 5000 employees |   1981|Private Practice / Firm|Consulting                              |Business Services        |$100 to $500 million (USD)|-1                                                    |
    3|Data Scientist                          |$137K-$171K (Glassdoor est.)|JOB DESCRIPTION:¶¶Do you have a passion for Data and Machine Learning? Do you dream of working with customers on their most forward-looking AI initiatives? Does the challenge of developing modern machine learning solutions to solve real-world manufacturin|   3.5|INFICON¶3.5           |Newton, MA       |Bad Ragaz, Switzerland|501 to 1000 employees  |   2000|Company - Public       |Electrical & Electronic Manufacturing   |Manufacturing            |$100 to $500 million (USD)|MKS Instruments, Pfeiffer Vacuum, Agilent Technologies|
    4|Data Scientist                          |$137K-$171K (Glassdoor est.)|Data Scientist¶Affinity Solutions / Marketing Cloud seeks smart, curious, technically savvy candidates to join our cutting-edge data science team. We hire the best and brightest and give them the opportunity to work on industry-leading technologies.¶The d|   2.9|Affinity Solutions¶2.9|New York, NY     |New York, NY          |51 to 200 employees    |   1998|Company - Private      |Advertising & Marketing                 |Business Services        |Unknown / Non-Applicable  |Commerce Signals, Cardlytics, Yodlee                  |
    5|Data Scientist                          |$137K-$171K (Glassdoor est.)|About Us:¶¶Headquartered in beautiful Santa Barbara, HG Insights is the global leader in technology intelligence. HG Insights uses advanced data science methodologies to help the world's largest technology firms and the fastest growing companies accelerat|   4.2|HG Insights¶4.2       |Santa Barbara, CA|Santa Barbara, CA     |51 to 200 employees    |   2010|Company - Private      |Computer Hardware & Software            |Information Technology   |Unknown / Non-Applicable  |-1                                                    |
    6|Data Scientist / Machine Learning Expert|$137K-$171K (Glassdoor est.)|Posting Title¶Data Scientist / Machine Learning Expert¶¶04-Feb-2020¶¶Job ID¶288341BR¶¶Job Description¶ONE Global Discovery Chemistry Community working across 7 disease areas at the Novartis Institutes for BioMedical Research (NIBR) is seeking a highly tal|   3.9|Novartis¶3.9          |Cambridge, MA    |Basel, Switzerland    |10000+ employees       |   1996|Company - Public       |Biotech & Pharmaceuticals               |Biotech & Pharmaceuticals|$10+ billion (USD)        |-1                                                    |
    7|Data Scientist                          |$137K-$171K (Glassdoor est.)|Introduction¶¶Have you always wanted to run experiments on a global fleet of consumer robots? iRobot is looking for a data scientist to help manage a/b tests related to robot software, track performance KPIs, and share results with software teams. A stron|   3.5|iRobot¶3.5            |Bedford, MA      |Bedford, MA           |1001 to 5000 employees |   1990|Company - Public       |Consumer Electronics & Appliances Stores|Retail                   |$1 to $2 billion (USD)    |-1                                                    |
    8|Staff Data Scientist - Analytics        |$137K-$171K (Glassdoor est.)|Intuit is seeking a Staff Data Scientist to cover Intuits Consumer Group (TurboTax, Mint, Turbo). We have an exciting opportunity to help shape how we use data to generate hypotheses, surface insights, and build models in order to personalize customer exp|   4.4|Intuit - Data¶4.4     |San Diego, CA    |Mountain View, CA     |5001 to 10000 employees|   1983|Company - Public       |Computer Hardware & Software            |Information Technology   |$2 to $5 billion (USD)    |Square, PayPal, H&R Block                             |
    9|Data Scientist                          |$137K-$171K (Glassdoor est.)|Ready to write the best chapter of your career? XSELL Technologies is an artificial intelligence company focused on increasing sales. Our cloud-based machine learning engine uses predictive analytics and natural language processing to equip sales professi|   3.6|XSELL Technologies¶3.6|Chicago, IL      |Chicago, IL           |51 to 200 employees    |   2014|Company - Private      |Enterprise Software & Network Solutions |Information Technology   |Unknown / Non-Applicable  |-1                                                    |















