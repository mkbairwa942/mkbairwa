from kiteconnect import KiteConnect
import pprint


key = "api_key"   # change

kite = KiteConnect(api_key=key)

access_token = "access_token"   # change

kite.set_access_token(access_token=access_token)

instruments_list = ["ReliAnce", 'Tatamotors', 'tCs', "upl"]

stocks_list = []
for i in instruments_list:
    stocks_list.append(f"NSE:{i.upper()}")

ticks = kite.quote(stocks_list)

live_data = {}
for k, v in ticks.items():
    live_data[k[4:]] = {"Open": v["ohlc"]["open"],
                        "High": v["ohlc"]["high"],
                        "Low": v["ohlc"]["low"],
                        "Ltp": v["last_price"],
                        "Vwap": v["average_price"],
                        "Volume": v["volume"]}


pprint.pprint(live_data)

# print(live_data["RELIANCE"])

# print(live_data["UPL"]['Ltp'])
# print(live_data["TATAMOTORS"]['Volume'])


