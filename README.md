# NN Mutual Fund #
## Information ##
Script to save the daily quote for the NN Moderate RON mutual fund in a Google Sheet document
## Configuration ##
Create a `config.ini` file:
```
[NN]
url = https://markets.ft.com/data/funds/tearsheet/historical?s=LU1505916277:RON

[Google]
auth = file name
excel = excel file
sheet = sheet name

[Loki]
app = name
url = http://127.0.0.1/
```
Don't forget to create the JSON file for Google authentification