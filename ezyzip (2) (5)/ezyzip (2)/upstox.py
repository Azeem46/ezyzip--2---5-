import json
import requests
import urllib.parse
import pandas as pd

apiKey = 'cb3588f7-b79f-4be7-8d5c-703e91d98d5a'
secretKey = 'hn558zfk9j'
rurl = urllib.parse.quote('https://127.0.0.1:5000/', safe="")  
uri = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={apiKey}&redirect_uri={rurl}'
print(uri)

code = 'dL4ctG'

url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json', 
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': code,
    'client_id': apiKey,
    'client_secret': secretKey,
    'redirect_uri': 'https://127.0.0.1:5000/',
    'grant_type': 'authorization_code',
}

response = requests.post(url, headers=headers, data=data)
json_response = response.json()
print(json_response)

# Check if 'access_token' exists in the response
if 'access_token' in json_response:
    access_token = json_response['access_token']
    print(access_token)
else:
    print("Error: 'access_token' not found in response")



#Getting the data of funds and margin

url = 'https://api.upstox.com/v2/user/get-funds-and-margin'
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}',  # Use the obtained access token
}

params = {'segment': 'SEC'}

response = requests.get(url, headers=headers, params=params)
print(response.status_code)
print(response.json())


fileurl="ezyzip (2)\complete.csv\complete.csv"
symboldf=pd.read_csv(fileurl)
symboldf['expiry']=pd.to_datetime(symboldf['expiry']).apply(lambda x: x.date())
print(symboldf)

niftydf=symboldf[(symboldf.instrument_type=="OPTIDX") & (symboldf.tradingsymbol.str.startswith('BANKNIFTY')) & (symboldf.exchange=='NSE_FO')]
print(niftydf)

expiryList=niftydf['expiry'].unique().tolist()
expiryList.sort()
print(expiryList)

print(expiryList[0])



print(symboldf[symboldf.tradingsymbol=='HDFC'])
print(symboldf[(symboldf.instrument_type=="FUTCOM") & (symboldf.tradingsymbol.str.startswith('SILVERMIC'))])


#Taking the market data 

# Define the API endpoint
url = 'https://api-v2.upstox.com/market-quote/quotes'

# Define the headers
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}',  # Replace {access_token} with your actual access token
}

# Define the parameters
params = {
    'symbol': 'NSE_EQ|INE848E01016,NSE_FO|43286'
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Output the response
print(response)
print(response.json())


#Making the request for api

def make_request(method, url, headers=None, params=None, data=None):
    response = None

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data)
        else:
            raise ValueError('Invalid HTTP method.')

        if response.status_code == 200:
            return response.json()
        else:
            return response

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

#this is the code for ohlc





url = "https://api.upstox.com/v2/market-quote/ohlc"

headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {access_token}',
}
params = {                                                                    
    'symbol': 'NSE_EQ|INE001A01036,NSE_FO|43286',
    'interval': 'I30'
}

response = requests.request("GET", url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()  # Get the data as a Python dictionary
    print(data)  # Print the dictionary in a readable format
else:
    print(f"Error: {response.status_code}")

url = 'https://api-v2.upstox.com/market-quote/ltp'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Authorization': f'Bearer {access_token}'
}
params = {
    'symbol': 'NSE_EQ|INE848E01016,NSE_EQ|INE001A01036'
}

response = make_request('GET', url, headers=headers, params=params)
print(response)




url = 'https://api-v2.upstox.com/historical-candle/NSE_EQ%7CINE848E01016/month/2024-05-01/2022-10-01'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0'
}

response = make_request('GET', url, headers=headers)
print(response)

"""
#place order on upstox
url = 'https://api-v2.upstox.com/order/place'


headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

data = {
    "quantity": 1,
    "product": "D",
    "validity": "DAY",
    "price": 23.90,
    "tag": "string",
    "instrument_token": "NSE_EQ|INE528G01035",
    "order_type": "LIMIT",
    "transaction_type": "BUY",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())

#this is for SELL
url = 'https://api-v2.upstox.com/order/place'


headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}

data = {
    "quantity": 1,
    "product": "D",
    "validity": "DAY",
    "price": 24,
    "tag": "string",
    "instrument_token": "NSE_EQ|INE528G01035",
    "order_type": "LIMIT",
    "transaction_type": "SELL",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
"""

bn="https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
df=pd.read_csv(bn)
def filter_df(df, lot_size):
    df = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTIDX') & (df['lot_size'] == lot_size)]
    df = df[df['expiry'] == min(df['expiry'].unique())]
    return df

BNDF = filter_df(df, 15)
BNDF[(BNDF['strike'] == 53100) & (BNDF['option_type'] == 'PE')]['instrument_key']
print(BNDF)


url = 'https://api-v2.upstox.com/order/place'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
payload={"quantity": 15,
    "product": "D",
    "validity": "DAY",
    "price": 0   ,
    "tag": "string",
    "instrument_token": "NSE_FO|63895",
    "order_type": "MARKET",
    "transaction_type": "BUY",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

data=json.dumps(payload)

response = requests.post(url, headers=headers, data=data)
print(response.json())
 

bn="https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
df=pd.read_csv(bn)
def filter_df(df, lot_size):
    df = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTIDX') & (df['lot_size'] == lot_size)]
    df = df[df['expiry'] == min(df['expiry'].unique())]
    return df

BNDF = filter_df(df, 15)
BNDF[(BNDF['strike'] == 53100) & (BNDF['option_type'] == 'PE')]['instrument_key']
print(BNDF)


url = 'https://api-v2.upstox.com/order/place'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
payload={"quantity": 15,
    "product": "D",
    "validity": "DAY",
    "price": 0   ,
    "tag": "string",
    "instrument_token": "NSE_FO|63895",
    "order_type": "MARKET",
    "transaction_type": "SELL",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

data=json.dumps(payload)

response = requests.post(url, headers=headers, data=data)
print(response.json())



#this is order of BUY
"""
bn="https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
df=pd.read_csv(bn)
def filter_df(df, lot_size):
    df = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTSTK') & (df['lot_size'] == lot_size)]
    df = df[df['expiry'] == min(df['expiry'].unique())]
    return df

BNDF = filter_df(df, 750)
BNDF[(BNDF['strike'] == "850") & (BNDF['option_type'] == 'CE')]['instrument_key']
print(BNDF)


url = 'https://api-v2.upstox.com/order/place'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
payload={"quantity": 750,
    "product": "D",
    "validity": "DAY",
    "price": 11.20 ,
    "tag": "string",
    "instrument_token": "NSE_FO|118892",
    "order_type": "LIMIT",
    "transaction_type": "BUY",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

data=json.dumps(payload)

response = requests.post(url, headers=headers, data=data)
print(response.json())
"""
bn="https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"
df=pd.read_csv(bn)
def filter_df(df, lot_size):
    df = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTSTK') & (df['lot_size'] == lot_size)]
    df = df[df['expiry'] == min(df['expiry'].unique())]
    return df

BNDF = filter_df(df, 750)
BNDF[(BNDF['strike'] == "850") & (BNDF['option_type'] == 'CE')]['instrument_key']
print(BNDF)


url = 'https://api-v2.upstox.com/order/place'
headers = {
    'accept': 'application/json',
    'Api-Version': '2.0',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
payload={"quantity": 750,
    "product": "D",
    "validity": "DAY",
    "price": 11.20 ,
    "tag": "string",
    "instrument_token": "NSE_FO|118892",
    "order_type": "LIMIT",
    "transaction_type": "SELL",
    "disclosed_quantity": 0,
    "trigger_price": 0,
    "is_amo": False
}

data=json.dumps(payload)

response = requests.post(url, headers=headers, data=data)
print(response.json())