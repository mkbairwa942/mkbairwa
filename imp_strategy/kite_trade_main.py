from kite_trade import *
import pandas as pd
import pyotp
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

user_id = "YR6706"       # Login Id
password = "vaa6762m"      # Login password
twofa = "404811"         # Login Pin or TOTP
TOTP=pyotp.TOTP("X3IFPEPCYJUPT2YMOYFTL5BJZ4VVF3F7").now()
print(user_id, password, TOTP)


mukesh = get_enctoken(user_id, password, TOTP)
credi_mukesh = KiteApp(mukesh)

enctoken = "JpWFQuzNYNiE0cQweFyxUjT7NZ8TKsjR7I3IyxQQUgrF7tPA52WTgyGgjSpObyR9Tnv9Ym409AqIKtZn8VciDIwB6kDkpanP0eqFUUmFS5m3gICiua8Reg=="
kite = KiteApp(enctoken=enctoken)

# print(credi_mukesh.margins())
# print(credi_mukesh.orders())
# print(credi_mukesh.positions())

# print(pd.DataFrame(kite.instruments()).tail(5))
# print(kite.instruments("NSE"))
# print(kite.instruments("NFO"))

# Get Live Data
# print(kite.ltp("NSE:RELIANCE"))
# # print(kite.ltp(["NSE:NIFTY 50", "NSE:NIFTY BANK"]))
# print(kite.quote(["NSE:NIFTY BANK", "NSE:ACC", "NFO:NIFTY22SEPFUT"]))

# # Get Historical Data
# import datetime
# instrument_token = 256265
# from_datetime = datetime.datetime.now() - datetime.timedelta(days=3)     # From last & days
# to_datetime = datetime.datetime.now()
# interval = "5minute"
# print(pd.DataFrame(credi_mukesh.historical_data(256265, from_datetime, to_datetime, interval, continuous=False, oi=True)))


# # Place Order
# order = kite.place_order(variety=kite.VARIETY_REGULAR,
#                          exchange=kite.EXCHANGE_NSE,
#                          tradingsymbol="ACC",
#                          transaction_type=kite.TRANSACTION_TYPE_BUY,
#                          quantity=1,
#                          product=kite.PRODUCT_MIS,
#                          order_type=kite.ORDER_TYPE_MARKET,
#                          price=None,
#                          validity=None,
#                          disclosed_quantity=None,
#                          trigger_price=None,
#                          squareoff=None,
#                          stoploss=None,
#                          trailing_stoploss=None,
#                          tag="TradeViaPython")

# print(order)

# # Modify order
# kite.modify_order(variety=kite.VARIETY_REGULAR,
#                   order_id="order_id",
#                   parent_order_id=None,
#                   quantity=5,
#                   price=200,
#                   order_type=kite.ORDER_TYPE_LIMIT,
#                   trigger_price=None,
#                   validity=kite.VALIDITY_DAY,
#                   disclosed_quantity=None)

# # Cancel order
# kite.cancel_order(variety=kite.VARIETY_REGULAR,
#                   order_id="order_id",
#                   parent_order_id=None)

# instruments = 'NFO:BANKNIFTY2432047100PE'
# while True:
#     inst  = credi_mukesh.quote(instruments)
#     data = pd.DataFrame.from_dict(inst)
#     #print(data)
#     print(inst)
#     print(data)
