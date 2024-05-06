## Project goal
Solve SQL exercises from popular online sources, such as DataLemur and Leetcode, to hone my SQL skills and make them even stronger. I chose these platforms since they provide real-life questions and challenges from existing worldwide companies.

## Exercises

#### User's Third Transaction _(DataLemur)_
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
