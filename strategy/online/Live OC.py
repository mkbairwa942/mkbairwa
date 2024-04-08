import requests
import json
import pandas as pd
import xlwings  as xw

pd.set_option('display.width',1500)
pd.set_option('display.max_columns',75)
pd.set_option('display.max_rows',1500)

url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
         'accept-language':'en-US,en;q=0.9,bn;q=0.8','accept-encoding':'gzip, deflate, br'}
expiry="06-Oct-2022"
excel_file="MyOC.xlsx"
wb= xw.Book(excel_file)
sheet_oi_single = wb.sheets("OIdata")
def fetch_oi():
    r = requests.get(url, headers=headers).json()

    if expiry:
        ce_values = [data['CE'] for data in r['records']['data'] if "CE" in data and str(data['expiryDate']).lower() == str(expiry).lower()]
        pe_values = [data['PE'] for data in r['records']['data'] if "PE" in data and str(data['expiryDate']).lower() == str(expiry).lower()]
    else:
        ce_values = [data['CE'] for data in r['filtered']['data'] if "CE" in data]
        pe_values = [data['PE'] for data in r['filtered']['data'] if "PE" in data]
    ce_data = pd.DataFrame(ce_values)
    pe_data = pd.DataFrame(pe_values)
    ce_data = ce_data.sort_values(["strikeprice"])
    pe_data = pe_data.sort_values(["strikeprice"])
    sheet_oi_single.range("A2").options().value= ce_data




def main():
    fetch_oi()






