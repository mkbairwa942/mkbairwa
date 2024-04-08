import requests
from bs4 import BeautifulSoup
import pandas as pd

Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'

#You need to copy paste condition in below mentioned Condition variable

Condition = "( {57960} ( [0] 15 minute close > [-1] 15 minute max ( 20 , [0] 15 minute close ) and [0] 15 minute volume > [0] 15 minute sma ( volume,20 ) ) ) "

def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            df = df.append(item, ignore_index=True)
    return df

data = GetDataFromChartink(Condition)

data = data.sort_values(by='per_chg', ascending=False)

print(data)

data.to_csv("Chartink_result.csv")