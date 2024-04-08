#!/usr/bin/env python
# coding: utf-8

# ## Install upstox SDK

# In[2]:


pip install upstox-python-sdk


# In[ ]:





# ## Set Acces Token and Download master List

# In[ ]:





# In[1]:


access_token = ''


# In[2]:


import pandas as pd
fileUrl ='https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
symboldf = pd.read_csv(fileUrl)
symboldf['expiry'] = pd.to_datetime(symboldf['expiry']).apply(lambda x: x.date())   
symboldf


# In[6]:


symboldf[(symboldf.tradingsymbol=='SAIL') & (symboldf.exchange == 'NSE_EQ') ]


# ## Order API

# In[3]:


from __future__ import print_function
import time
import upstox_client
from upstox_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAUTH2
configuration = upstox_client.Configuration()
configuration.access_token = access_token

# create an instance of the API class
api_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

api_version = '2.0' # str | API Version Header



# In[18]:


try:
    # Place order
    body ={
    "quantity": 1,
    "product": "I",
    "validity": "DAY",
    "price": 0,
    "tag": "dft",
    "instrument_token": "NSE_EQ|INE114A01011",
    "order_type": "MARKET",
    "transaction_type": "BUY",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}
    api_response = api_instance.place_order(body, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->place_order: %s\n" % e)


# In[12]:


body ={
    "quantity": 1,
    "product": "I",
    "validity": "DAY",
    "price": 84.9,
    "order_id": "231107000471261",
    
    "order_type": "LIMIT",
   

    "trigger_price": 0,

}


try:
    # Modify order
    api_response = api_instance.modify_order(body, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->modify_order: %s\n" % e)


# In[13]:


try:
    # Cancel order
    order_id  = '231107000471261'
    api_response = api_instance.cancel_order(order_id, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->cancel_order: %s\n" % e)


# In[ ]:


try:
    # Get order book
    api_response = api_instance.get_order_book(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_book: %s\n" % e)


# In[ ]:


order_id = '231107000471261' # str | The order reference ID for which the order history is required (optional)


try:
    # Get order details
    api_response = api_instance.get_order_details(api_version, order_id=order_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OrderApi->get_order_details: %s\n" % e)


# In[19]:


# create an instance of the API class
api_instance = upstox_client.PortfolioApi(upstox_client.ApiClient(configuration))


try:
    # Get Positions
    api_response = api_instance.get_positions(api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortfolioApi->get_positions: %s\n" % e)


# In[20]:


# create an instance of the API class
api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_EQ|INE114A01011' # str | 
interval = '1minute' # str | 
to_date = '2023-10-15' # str | 


try:
    # Historical candle data
    api_response = api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HistoryApi->get_historical_candle_data: %s\n" % e)


# In[6]:


import pandas as pd
from datetime import datetime
from time import sleep


# In[17]:


api_instance = upstox_client.HistoryApi()
instrument_key = 'NSE_FO|42690' # str | 
interval = '1minute' # str | 
api_version = '2.0'
try:
    # Intra day candle data
    #sleep(60-datetime.now().second)
    api_response = api_instance.get_intra_day_candle_data(instrument_key, interval, api_version).to_dict()
    candleData = pd.DataFrame(api_response['data']['candles'])
    candleData.columns = ['date','open','high','low', 'close','volume','oi']
    candleData['date'] = pd.to_datetime(candleData['date']).dt.tz_convert('Asia/Kolkata')
    candleData = candleData.sort_values(by='date')
    print(datetime.now(),candleData.iloc[-1] ['date'])
    #display(candleData.tail(2))
except ApiException as e:
    print("Exception when calling HistoryApi->get_intra_day_candle_data: %s\n" % e)
    


# In[ ]:




