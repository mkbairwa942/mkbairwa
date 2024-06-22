import numpy as np
import pandas as pd
from datetime import datetime,timedelta
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta,gamma,rho,theta


# variables

S = 23501.10
K = 23400
r = 0.10
T = 5/365
sigma = 0.633
price = 165.15
flag = 'c'

T = (datetime(2024,6,27,15,30,0)-datetime(2024,6,21,15,30,0))/timedelta(days=1)/365
dt = datetime(2024,6,27,15,30,0)-datetime.now()
print(dt)
print(T)

d1 = (np.log(S/K)+((r+sigma**2/2)*T))/(sigma*np.sqrt(T))
print(d1)
d2 = d1-(sigma*np.sqrt(T))
print(d2)
call = S*norm.cdf(d1,0,1)-norm.cdf(d2,0,1)*K*np.exp(-r*T)
print(call)
put = norm.cdf(-d2,0,1)*K*np.exp(-r*T)-S*norm.cdf(-d1,0,1)
print(put)
Call_price = bs('c',S,K,T,r,sigma)
print(Call_price)
Put_price = bs('p',S,K,T,r,sigma)
print(Put_price)

iv = implied_volatility(price,S,K,T,r,flag)
print(iv)
deltaa = delta(flag,S,K,T,r,iv)
print(deltaa)
rhoo = rho(flag,S,K,T,r,iv)
print(rhoo)
gamaa = gamma(flag,S,K,T,r,iv)
print(gamaa)
thetaa = theta(flag,S,K,T,r,iv)
print(thetaa)