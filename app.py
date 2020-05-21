import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread

url = 'https://markets.ft.com/data/funds/tearsheet/historical?s=LU1505916277:RON'
path = '/html/body/div[3]/div[2]/section[3]/div[1]/div/div/div[2]/div[2]/table/tbody/tr[1]/td[1]'
page = requests.get(url)

if page.status_code != 200:
    print('Error in GET of page')
    exit()

soup = BeautifulSoup(page.text, 'html.parser')

# Get date for the first entry in table
date_str = soup.body.tbody.tr.span.contents[0]
# Get value for the first entry in table 
value = soup.body.tbody.tr.contents[4].string

# Convert string date to object
date = datetime.strptime(date_str, '%A, %B %d, %Y')

# Get and open spreadsheet
gc = gspread.service_account(filename='service_account.json')
sh = gc.open('NN RON Moderat')
worksheet = sh.worksheet('Sheet')

# Prepare row information
c_date = date.strftime('%m/%d/%Y')
c_price = value
c_delta = '=B2-B3'
c_percent = '=ROUND(C2/B3*100,3)'
row = [c_date, c_price, c_delta, c_percent]

# Check if row already exists
ex_date = worksheet.get('A2').first()
if date.strftime('%A, %B %d, %Y') == ex_date:
    print('Entry already exists')
    exit()

# Insert new row
worksheet.insert_row(row, index=2, value_input_option='USER_ENTERED')
