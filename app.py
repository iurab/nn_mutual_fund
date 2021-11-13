import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
import time
import json
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')


def get_new_price():

    page = requests.get(CONFIG['NN']['url'])

    if page.status_code != 200:
        message = 'HTTP GET was not successful for {}'.format(CONFIG['NN']['url'])
        log('error', message)
        exit()

    soup = BeautifulSoup(page.text, 'html.parser')

    # Get date for the first entry in table
    date_str = soup.body.tbody.tr.span.contents[0]
    # Get value for the first entry in table
    value = soup.body.tbody.tr.contents[4].string

    # Convert string date to object
    date = datetime.strptime(date_str, '%A, %B %d, %Y')

    # Get and open spreadsheet
    gc = gspread.service_account(filename=CONFIG['Google']['auth'])
    sh = gc.open(CONFIG['Google']['excel'])
    worksheet = sh.worksheet(CONFIG['Google']['sheet'])

    # Prepare row information
    c_date = date.strftime('%m/%d/%Y')
    c_price = value
    c_delta = '=B2-B3'
    c_percent = '=ROUND(C2/B3*100,3)'
    row = [c_date, c_price, c_delta, c_percent]

    # Check if row already exists
    ex_date = worksheet.get('A2').first()
    if date.strftime('%A, %B %d, %Y') == ex_date:
        message = 'Entry already present: {}'.format(row[:2])
        # log('warning', message)
        exit()

    # Insert new row
    worksheet.insert_row(row, index=2, value_input_option='USER_ENTERED')
    message = 'New entry added: {}'.format(row[:2])
    # Loki doesn't exists anymore
    # log('info', message)


def log(level, message):
    headers = {'Content-type': 'application/json'}

    timestamp = int(time.time()) * 10**9

    data = {
        'streams': [{
            'stream': {
                'app': CONFIG['Loki']['app'],
                'level': level,
            },
            'values': [[str(timestamp), message]]
        }]
    }
    r = requests.put(CONFIG['Loki']['url'],
                     headers=headers,
                     data=json.dumps(data))


if __name__ == '__main__':
    get_new_price()