#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install --upgrade pandas_ta


# In[ ]:


import pandas as pd
import pandas_ta as ta


# In[ ]:


df = pd.read_csv('sbin5min.csv')
df


# In[ ]:


help(ta.supertrend)


# In[ ]:


sup = ta.supertrend(high=df['high'], low=df['low'], close=df['close'], length=7, multiplier=3)


# In[ ]:


dfs = pd.concat([df, sup], axis=1)
dfs


# In[ ]:


help(ta.ha)


# In[ ]:


hkCandle = ta.ha(df['open'], df['high'], df['low'],df['close'])
hkCandle


# In[ ]:


df_hk = pd.concat([df, hkCandle], axis=1)
df_hk


# In[ ]:


df.ta.indicators()

