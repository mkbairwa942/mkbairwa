from kite_trade import *
import pandas as pd
from py_vollib.black_scholes.implied_volatility import implied_volatility
from py_vollib.black_scholes.greeks.analytical import delta, gamma, rho, theta, vega

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.options.mode.chained_assignment = None

# user_id = "YR6706"       # Login Id
# password = "vaa6762m"      # Login password
# twofa = "274957"         # Login Pin or TOTP

# enctoken = get_enctoken(user_id, password, twofa)
# kite = KiteApp(enctoken=enctoken)

enctoken = "gQ/zLVyhmVCyuSSga5+qu+44S7z7kcKiOfb1eww3FYFrhVfgG/0pUuTcpc5Kz0yYWInqvFG1XZT+9CKGNf8Za4LEWssj1r0UnZcaQnO/NiuuvETXs9trrA=="
kite = KiteApp(enctoken=enctoken)

# print(kite.margins())
# print(kite.orders())
# print(kite.positions())

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
# from_datetime = datetime.datetime.now() - datetime.timedelta(days=7)     # From last & days
# to_datetime = datetime.datetime.now()
# interval = "5minute"
# print(kite.historical_data(instrument_token, from_datetime, to_datetime, interval, continuous=False, oi=False))


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

instruments = 'NFO:BANKNIFTY2362944400PE'

inst  = kite.quote(instruments)
data = pd.DataFrame.from_dict(inst)
#print(data)
print(inst)
