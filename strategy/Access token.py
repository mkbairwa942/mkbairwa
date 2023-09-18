from kiteconnect import KiteConnect

key = "api_key"    # change
secret = "api_secret"   # change

kite = KiteConnect(api_key=key)

print("Login here :", kite.login_url())

req_tkn = input("Enter request token here : ")

gen_ssn = kite.generate_session(request_token=req_tkn, api_secret=secret)

acc_tkn = gen_ssn['access_token']

print(acc_tkn)

kite.set_access_token(access_token=acc_tkn)

# save in file
