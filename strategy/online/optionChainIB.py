#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from breeze_connect import BreezeConnect
import pandas as pd
import time
import urllib


# In[ ]:


api_key = 'your_API_KEY'
api_secret = 'your_SECRET_KEY'


# In[ ]:


session_key = '2072145'


# In[ ]:


print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus(api_key))


# In[ ]:


breeze = BreezeConnect(api_key=api_key)

breeze.generate_session(api_secret=api_secret,session_token=session_key)
breeze.get_funds()


# In[ ]:


import xlwings as xw
wb = xw.Book(r'C:\Users\hari\Desktop\demoXlwing.xlsx')
sheet = wb.sheets['Sheet2']


# In[ ]:


for i in range(1,10):
    res = breeze.get_option_chain_quotes(stock_code="CNXBAN",
                        exchange_code="NFO",
                        product_type="options",
                        expiry_date="2022-12-29T06:00:00.000Z" ,
                                        right="others",)
    ocdf = pd.DataFrame(res['Success'])
    ocdf = ocdf[ocdf.open_interest > 0]
    ocdf.sort_values(by = 'strike_price',inplace =True)
    ocdf = ocdf[['right','open_interest','chnge_oi','ltp','best_offer_price','best_bid_price','ltp_percent_change','strike_price']]
    ceocdf = ocdf[ocdf.right == 'Call']
    peocdf = ocdf[ocdf.right == 'Put']
    finalOC= ceocdf.merge(peocdf,on = 'strike_price',how='outer')
    finalOC.fillna('',inplace =True)
    finalOC.sort_values(by = 'strike_price',inplace =True)
    sheet['D6'].options(index=False).value = finalOC
    time.sleep(5)


# In[ ]:




