## Project goal
Solve SQL exercises from popular online sources, such as DataLemur and Leetcode, to hone my SQL skills and make them even stronger. I chose these platforms since they provide real-life questions and challenges from existing worldwide companies.

## Exercises

#### 1. User's Third Transaction _(DataLemur)_
Assume you are given the table below on Uber transactions made by users. Write a query to obtain the third transaction of every user. Output the user id, spend and transaction date.

``` sql
WITH numbered_transactions AS (
  SELECT user_id,
         spend,
         transaction_date,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY transaction_date) AS row_num
  FROM transactions
)
SELECT user_id,
       spend,
       transaction_date
FROM numbered_transactions
WHERE row_num = 3;
```

#### 2. Sending vs. Opening Snaps _(DataLemur)_
Assume you're given tables with information on Snapchat users, including their ages and time spent sending and opening snaps. Write a query to obtain a breakdown of the time spent sending vs. opening snaps as a percentage of total time spent on these activities grouped by age group. Round the percentage to 2 decimal places in the output.

```sql
SELECT 
  age.age_bucket, 
  ROUND(100.0 * 
    SUM(activities.time_spent) FILTER (WHERE activities.activity_type = 'send')/
      SUM(activities.time_spent),2) AS send_perc, 
  ROUND(100.0 * 
    SUM(activities.time_spent) FILTER (WHERE activities.activity_type = 'open')/
      SUM(activities.time_spent),2) AS open_perc
FROM activities
INNER JOIN age_breakdown AS age 
  ON activities.user_id = age.user_id 
WHERE activities.activity_type IN ('send', 'open') 
GROUP BY age.age_bucket;
```

#### 3. Highest-Grossing Items _(DataLemur)_
Assume you're given a table containing data on Amazon customers and their spending on products in different category, write a query to identify the top two highest-grossing products within each category in the year 2022. The output should include the category, product, and total spend.

```sql
WITH ranked_spen AS (
  SELECT 
    category, 
    product, 
    SUM(spend) AS total_spend,
    RANK() OVER (
      PARTITION BY category 
      ORDER BY SUM(spend) DESC) AS ranking 
  FROM product_spend
  WHERE EXTRACT(YEAR FROM transaction_date) = 2022
  GROUP BY category, product
)

SELECT 
  category, 
  product, 
  total_spend 
FROM ranked_spend 
WHERE ranking <= 2
ORDER BY category, ranking
```
#### 4. Active User Retention _(DataLemur)_
Assume you're given a table containing information on Facebook user actions. Write a query to obtain number of monthly active users (MAUs) in July 2022, including the month in numerical format "1, 2, 3".

Hint: An active user is defined as a user who has performed actions such as 'sign-in', 'like', or 'comment' in both the current month and the previous month.


```sql
select 
current_month, count(distinct user_id)
from 
  (select user_id, 
    extract(month from event_date) as current_month, 
    case 
      when extract(month from event_date) - 
      coalesce(lag(extract(month from event_date)) over(partition by user_id order by extract(month from event_date)), -1) = 1
      then 'Active' else 'Inactive' 
    end as user_status
  from user_actions
  where event_type in ('like', 'comment')
  ) a
where user_status = 'Active'
group by current_month
```
#### 5. Median Google Search Frequency _(DataLemur)_
Google's marketing team is making a Superbowl commercial and needs a simple statistic to put on their TV ad: the median number of searches a person made last year.

However, at Google scale, querying the 2 trillion searches is too costly. Luckily, you have access to the summary table which tells you the number of searches made last year and how many Google users fall into that bucket.

Write a query to report the median of searches made by a user. Round the median to one decimal point.


```sql
WITH t1 AS (
  SELECT searches
  FROM search_frequency
  GROUP BY 
    searches, 
    GENERATE_SERIES(1, num_users))

SELECT 
  ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (
    ORDER BY searches)::DECIMAL, 1) AS  median
FROM t1;
```

