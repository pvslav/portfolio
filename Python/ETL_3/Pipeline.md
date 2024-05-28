# Data Pipeline 

In our project, we will design a code that extracts the top 10 largest banks in the world by market capitalization in billion USD. This list will be processed and stored in GBP and EUR currencies, utilizing the latest available exchange rates online.

The resulting data will be saved in both CSV format for local storage and as a database table for future reference.

Our task is to develop an automated system for generating this information, enabling us to prepare quarterly reports seamlessly and efficiently. This system will streamline our reporting process, reducing manual errors and enhancing our operational efficiency.

## Step 1. Extract data

We write a function that will parse the data we need from a table on the Wikipedia page.

```python
url = 'https://en.wikipedia.org/wiki/List_of_largest_banks'

def extract(url):
    df = pd.DataFrame(columns=["Rank", "Bank_Name", "Total_assets"])
    count = 0

    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        if count < 15:
            col = row.find_all('td')
            if len(col) != 0:
                rank = int(col[0].contents[0])
                bank_name = col[1].get_text(strip=True)
                total_assets = float(col[2].contents[0].replace(',', ''))
                data_dict = {"Rank": rank, "Bank_Name": bank_name, "Total_assets": total_assets}
                df = pd.concat([df, pd.DataFrame(data_dict, index=[0])], ignore_index=True)
                count += 1
        else:
            break
    
    return df

df = extract(url)
print(df)
```
