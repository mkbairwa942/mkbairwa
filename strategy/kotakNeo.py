#!/usr/bin/env python
# coding: utf-8

# In[ ]:


consumer_key = 'hjF4yqPwhvTCiviCNJDNMSEa'      
secretKey ='2EFd3UmD2OJ23cBdh7nJD0wga' 

username  ='client815'   # api portal username
password = 'hjdu8s'    # api portal pasword

user_id = 'ffbvyg-bhvgbnm-fbjfcbh'
mobileNumber = '+919876543211'
login_password = 'dft@12345'   #login password use to login broker web platform


# In[ ]:


import urllib.parse
import base64
import requests
import json


# In[ ]:


ses = requests.Session()
url = "https://napi.kotaksecurities.com/oauth2/token"
code = f'{consumer_key}:{secretKey}'
payload = { 'grant_type': 'password','username': username , 'password':password}
headers = {"Authorization": f"Basic {base64.b64encode(bytes(code, 'utf-8')).decode('utf-8')}" }

response = ses.post( url, headers=headers, data=payload)

tokenResposne = response.json()
access_token = tokenResposne['access_token']
tokenResposne


# In[ ]:


import requests
import json

url = "https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate"

payload = json.dumps({
  "mobileNumber": mobileNumber,
  "password": login_password
})
headers = {
  'accept': '*/*',
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {access_token}'
}

response = ses.post(url, headers=headers, data=payload)

validityRes = response.json()
authtoken = validityRes['data']['token']
sid = validityRes['data']['sid']
hsServerId = validityRes['data']['hsServerId']
hsServerId , sid , authtoken


# In[ ]:





# In[ ]:


headers = {
   'accept': '*/*',
   'sid': sid,
   'Auth': authtoken,
   'neo-fin-key': 'neotradeapi',
   'Authorization': f'Bearer {access_token}',
   'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    
}


# In[ ]:




url = "https://gw-napi.kotaksecurities.com/login/1.0/login/otp/generate"

payload = json.dumps({
  "userId":userId,
  "sendEmail": True,
  "isWhitelisted": True
})


response = requests.request("POST", url, headers=headers, data=payload)


response.json()


# In[ ]:




url = "https://gw-napi.kotaksecurities.com/login/1.0/login/v2/validate"

payload = json.dumps({
  "userId": userId,
  "otp": "8086"
})


finalresponse = requests.request("POST", url, headers=headers, data=payload)

finalresponse.json()


# In[ ]:


# header updated here


headers = {
   'accept': '*/*',
   'sid': sid,
   'Auth': finalresponse.json()['data']['token'],
   'neo-fin-key': 'neotradeapi',
   'Authorization': f'Bearer {access_token}',
   'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    
}

params = {'sId' : hsServerId}


# In[ ]:



url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/user/limits"
reqLoad = {"seg": "CASH","exch": "NSE","prod": "ALL"}
payload = urllib.parse.urlencode({'jData': json.dumps(reqLoad)},quote_via=urllib.parse.quote)
response = ses.post(url, headers=headers, params = params,data=payload)

response.json()


# In[ ]:


#Holding

url = "https://gw-napi.kotaksecurities.com/Portfolio/1.0/portfolio/v1/holdings"

payload={}


response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


# In[ ]:


#Position
url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/user/positions"

payload={}

response = requests.request("GET", url, headers=headers, data=payload,params=params)

print(response.text)


# In[ ]:


url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/user/orders"

payload={}


response = requests.request("GET", url, headers=headers, data=payload,params= params)


# In[ ]:


import pandas as pd
orderdf  = pd.DataFrame(response.json()['data'])
orderdf = orderdf[['nOrdNo','ordSt','trdSym','trnsTp','exSeg','prod','tok','prc','prcTp','trgPrc','qty','ordDtTm','rejRsn']]
orderdf


# In[ ]:


#trade book
url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/user/trades"

payload={}

response = requests.request("GET", url, headers=headers, data=payload,params= params)

response.json()


# In[ ]:


url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/order/history"

jData = {"nOrdNo":"230127000663070"}
payload =  urllib.parse.urlencode({'jData': json.dumps(jData)},quote_via=urllib.parse.quote)


response = requests.request("POST", url, headers=headers, data=payload,params= params)


histdf=  pd.DataFrame(response.json()['data'])
histdf


# In[ ]:


histdf.columns


# In[ ]:


histdf[['avgPrc','ordSt','exchTmstp']]


# In[ ]:


url = "https://gw-napi.kotaksecurities.com/Files/1.0/masterscrip/file-paths"

payload={}

response = requests.request("GET", url, headers=headers, data=payload)

response.json()


# In[ ]:



fileRespnse= response.json()


# In[ ]:


symboldf = pd.read_csv(fileRespnse['data']['filesPaths'][0],header=None)
symboldf


# In[ ]:


symboldf.iloc[0].to_dict()


# In[ ]:


url =  'https://gw-napi.kotaksecurities.com/Orders/2.0/quick/order/rule/ms/place'

jData = {"am":"NO","dq":"0","es":"nse_cm","mp":"0","pc":"CNC","pf":"N","pr":"0","pt":"MKT",
         "qt":"1","rt":"DAY","tp":"0","ts":"ITC-EQ","tt":"B",}

    
payload = urllib.parse.urlencode({'jData': json.dumps(jData)},quote_via=urllib.parse.quote)
orderResponse =ses.post(url, headers=headers,data=payload,params = params, timeout=3)
orderResponse = orderResponse.json()
orderResponse


# In[ ]:


url = "https://gw-napi.kotaksecurities.com/Orders/2.0/quick/order/cancel"

jData={"on":"230127000665779","am":"NO"}

payload = urllib.parse.urlencode({'jData': json.dumps(jData)},quote_via=urllib.parse.quote)
response = requests.request("POST", url, headers=headers, data=payload,params = params)

print(response.text)


# In[ ]:




