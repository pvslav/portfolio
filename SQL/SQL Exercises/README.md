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

#### 6. Advertiser Status _(DataLemur)_
You're provided with two tables: the advertiser table contains information about advertisers and their respective payment status, and the daily_pay table contains the current payment information for advertisers, and it only includes advertisers who have made payments.

Write a query to update the payment status of Facebook advertisers based on the information in the daily_pay table. The output should include the user ID and their current payment status, sorted by the user id.

```sql
SELECT
  user_id,
  CASE
    WHEN paid IS NULL THEN 'CHURN'
    WHEN status = 'CHURN' AND paid IS NOT NULL THEN 'RESURRECT'
    WHEN status IS NULL AND paid IS NOT NULL THEN 'NEW'
    ELSE 'EXISTING'
  END AS new_status
FROM 
  advertiser FULL OUTER JOIN daily_pay USING(user_id)
ORDER BY 
  user_id
```
#### 7. 3-Topping Pizzas _(DataLemur)_

You’re a consultant for a major pizza chain that will be running a promotion where all 3-topping pizzas will be sold for a fixed price, and are trying to understand the costs involved.

Given a list of pizza toppings, consider all the possible 3-topping pizzas, and print out the total cost of those 3 toppings. Sort the results with the highest total cost on the top followed by pizza toppings in ascending order.

Break ties by listing the ingredients in alphabetical order, starting from the first ingredient, followed by the second and third.

```sql
SELECT
  CONCAT(p1.topping_name, ',', p2.topping_name, ',', p3.topping_name) AS pizza,
  p1.ingredient_cost + p2.ingredient_cost + p3.ingredient_cost AS total_cost
FROM
  pizza_toppings AS p1,
  pizza_toppings AS p2,
  pizza_toppings AS p3
WHERE
  p1.topping_name < p2.topping_name
  AND p2.topping_name < p3.topping_name
ORDER BY
  total_cost DESC,
  pizza ASC
```
#### 8. International Call Percentage _(DataLemur)_

A phone call is considered an international call when the person calling is in a different country than the person receiving the call. What percentage of phone calls are international? Round the result to 1 decimal. 

Assumption:

  The caller_id in phone_info table refers to both the caller and receiver.
    
```sql
SELECT
  ROUND(
    100.0 *
    SUM(CASE WHEN caller.country_id != receiver.country_id
          THEN 1 ELSE 0 END)
      /
    COUNT(*)
  , 1) AS international_calls_pct
FROM 
  phone_calls AS calls
    JOIN phone_info AS caller ON calls.caller_id = caller.caller_id
    JOIN phone_info AS receiver ON calls.receiver_id = receiver.caller_id
```

#### 9. Histogram of Users and Purchases _(DataLemur)_

Assume you're given a table on Walmart user transactions. Based on their most recent transaction date, write a query that retrieve the users along with the number of products they bought. Output the user's most recent transaction date, user ID, and the number of products, sorted in chronological order by the transaction date.

```sql
WITH last_user_transactions AS (
  SELECT 
    product_id,
    user_id,
    transaction_date,
    FIRST_VALUE(transaction_date) OVER(PARTITION BY user_id ORDER BY transaction_date DESC) AS recent_payment_date
  FROM 
    user_transactions
)
SELECT
  recent_payment_date,
  user_id,
  COUNT(DISTINCT product_id) AS purchase_count
FROM
  last_user_transactions
WHERE
  transaction_date = recent_payment_date
GROUP BY
  recent_payment_date,
  user_id
ORDER BY
  recent_payment_date
```

#### 10. Pharmacy Analytics  _(DataLemur)_

CVS Health is trying to better understand its pharmacy sales, and how well different drugs are selling.

Write a query to find the top 2 drugs sold, in terms of units sold, for each manufacturer. List your results in alphabetical order by manufacturer.

```sql
WITH sales_cte AS (
SELECT
  manufacturer,
  drug,
  RANK() OVER(PARTITION BY manufacturer ORDER BY units_sold DESC) AS rnk
FROM pharmacy_sales)
SELECT
  manufacturer,
  drug AS top_drugs
FROM sales_cte
WHERE rnk <= 2
ORDER BY manufacturer
```
