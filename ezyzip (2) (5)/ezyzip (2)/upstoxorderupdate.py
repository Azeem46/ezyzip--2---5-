from __future__ import print_function
from pprint import pprint
import upstox_client
import ssl
import websockets
from upstox_client.rest import ApiException
import asyncio
import json

ORDER_TAG = 'PLACE_SL'
SL_PRCNT = 0.5

configuration = upstox_client.Configuration()
api_version = '2.0'
configuration.access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI3UkFTQkQiLCJqdGkiOiI2NjcxMWZjODEwODU4OTM3ZGM2NDkxNTEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzE4Njg5NzM2LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MTg3NDgwMDB9.l6ggUZ6HsQUXbAxXTxZwKfk-cII5BjKhgLnsLl-VbVs'

orderApi_instance = upstox_client.OrderApi(upstox_client.ApiClient(configuration))

def truncate(f):
    if f is None or f == 0:
        return f
    f = round(f / 0.05) * 0.05  # tick size 0.05
    n = 2
    s = '%.*12f' % (n, f)
    i, d, p = s.partition('.')
    return float('.'.join([i, (d + p)[:n]]))

def get_portfolio_stream_feed_authorize(api_version, configuration):
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration)
    )
    api_response = api_instance.get_portfolio_stream_feed_authorize(
        api_version
    )
    return api_response
