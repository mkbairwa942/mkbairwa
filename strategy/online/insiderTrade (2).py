#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
pd.set_option('display.max_columns', None)
import requests
from datetime import datetime
from datetime import timedelta  
import json
import time

start_time = time.time()
fromdate = datetime.strftime(datetime.today(),'%d-%m-%Y')
todate =  datetime.today() - timedelta(days=120)  
enddate = datetime.strftime(todate,'%d-%m-%Y')
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.9","Accept-Encoding": "gzip, deflate, br"}
URL1 = "https://www.nseindia.com/companies-listing/corporate-filings-insider-trading"
d1 = requests.get(URL1,headers=head)

URL = 'https://www.nseindia.com/api/corporates-pit?index=equities&from_date='+ enddate+ '&to_date=' + fromdate
print(URL)
d = requests.get(URL,headers=head,cookies =d1.cookies ).json()
df = pd.DataFrame(d['data'])
df["secVal"].replace({"-": 0}, inplace=True)
df["secVal"] = pd.to_numeric(df["secVal"])
df["secAcq"] = pd.to_numeric(df["secAcq"])

personCat = ['Promoters','Promoter Group']
df = df[df['acqMode'] == 'Market Purchase']
df = df[df['personCategory'].isin(personCat) ]
df['acqfromDt'] = pd.to_datetime(df['acqfromDt'], format='%d-%b-%Y',errors='ignore')

df1 = df.groupby(['symbol']).agg({'secVal':'sum','secAcq':'sum','acqfromDt':'max'}).reset_index()
df1['BuyValue'] = round(df1['secVal']/df1['secAcq'],2)
df1 = df1[df1['secVal']  > 100000000]
df1.sort_values(by = 'acqfromDt',ascending = False)


# In[ ]:




