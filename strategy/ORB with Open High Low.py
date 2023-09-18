from kiteconnect import KiteConnect
import datetime, time
api_k = ""
api_s = ""
kite = KiteConnect(api_key=api_k)
# print(kite.generate_session(request_token=input(f"Request Token: {kite.login_url()} \n= "), api_secret=api_s)['access_token'])
# sys.exit()
kite.set_access_token(access_token="RCS3FAQHds0wdER4srrH3XTzemGmuh51")
history, instruments_list = {}, ["Reliance", 'Tatamotors', 'Tcs']
while datetime.time(9, 20) < datetime.datetime.now().time() < datetime.time(15, 15):
    for symbol, values in {k[4:]: {"Open": v["ohlc"]["open"], "High": v["ohlc"]["high"], "Low": v["ohlc"]["low"]} for k, v in kite.quote([f"NSE:{i.upper()}" for i in instruments_list]).items()}.items():
        try:
            history[symbol]
        except:
            history[symbol] = {"High": values["High"], "Low": values["Low"], "Traded": False}
        if values['High'] > history[symbol]['High'] and values["Open"] == values['Low'] and not history[symbol]['Traded']:
            print("Buy :", symbol, f" at {values['High']} and Time {datetime.datetime.now().time()}")
            history[symbol]['Traded'] = True
        if values['Low'] < history[symbol]['Low'] and values["Open"] == values['High'] and not history[symbol]['Traded']:
            print("Sell :", symbol, f" at {values['Low']} and Time {datetime.datetime.now().time()}")
            history[symbol]['Traded'] = True
    time.sleep(2)
print("Session Ended !!!!") if datetime.datetime.now().time() > datetime.time(15, 15) else print("Wait till 9:20 !!!!")
