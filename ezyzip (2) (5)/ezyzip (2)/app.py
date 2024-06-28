# import threading
# import asyncio
# import json
# import ssl
# from flask import Flask, render_template, redirect, url_for, request
# from upstox_api.api import Upstox, Session
# import upstox_client
# import websockets
# from google.protobuf.json_format import MessageToDict
# import MarketDataFeed_pb2 as pb
# import mysql

# app = Flask(__name__)

# api_key = 'cb3588f7-b79f-4be7-8d5c-703e91d98d5a'
# api_secret = 'hn558zfk9j'
# redirect_url = 'http://127.0.0.1:5000/'

# session = Session(api_key)
# upstox = None

# # Flask Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return redirect(url_for('dashboard'))
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == "POST":
#         signup = request.form
#         name = signup["name"]
#         number = signup["number"]
#         email = signup["email"]
#         username = signup["username"]
#         password = signup["password"]
#         mydb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="flaskapp"
#         )
#         mycursor = mydb.cursor()
#         mycursor.execute("INSERT INTO users(name, number, email, username, password) VALUES(%s, %s, %s, %s, %s)",
#                          (name, number, email, username, password))
#         mydb.commit()
#         mycursor.close()
#         return redirect(url_for('login'))
#     return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/add_edit_scrip')
# def add_edit_scrip():
#     return render_template('add_edit_scrip.html')

# @app.route('/time')
# def time():
#     return render_template('time.html')

# @app.route('/watch.html')
# def watch():
#     return render_template('watch.html')

# @app.route('/tmw', methods=['POST'])
# def tmw():
#     form_data = request.form
#     return render_template('tmw.html', form_data=form_data)

# @app.route('/fno_index.html')
# def fno_index():
#     return render_template('fno_index.html')

# @app.route('/callback')
# def callback():
#     global upstox
#     session.set_redirect_uri(redirect_url)
#     session.set_api_secret(api_secret)
#     code = request.args.get('code')
#     session.set_code(code)
#     access_token = session.retrieve_access_token()
#     upstox = Upstox(api_key, access_token)
#     return redirect(url_for('dashboard'))

# def get_market_data_feed_authorize(api_version, configuration):
#     api_instance = upstox_client.WebsocketApi(
#         upstox_client.ApiClient(configuration))
#     api_response = api_instance.get_market_data_feed_authorize(api_version)
#     return api_response

# def decode_protobuf(buffer):
#     feed_response = pb.FeedResponse()
#     feed_response.ParseFromString(buffer)
#     return feed_response

# async def fetch_market_data():
#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE

#     configuration = upstox_client.Configuration()
#     api_version = '2.0'
#     configuration.access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI3UkFTQkQiLCJqdGkiOiI2NjdkMTI4NjNjOGJhNDE5NWJhMzliMTkiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzE5NDcyNzc0LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MTk1MjU2MDB9.hNIuxcLqERPQBdecf341Lj2dXIw8aLbjumm4kOM5Xn0'
#     response = get_market_data_feed_authorize(api_version, configuration)

#     async with websockets.connect(response.data.authorized_redirect_uri, ssl=ssl_context) as websocket:
#         data = {
#             "guid": "someguid",
#             "method": "sub",
#             "data": {
#                 "mode": "full",
#                 "instrumentKeys": ["NSE_INDEX|Nifty Bank", "NSE_INDEX|Nifty 50"]
#             }
#         }

#         binary_data = json.dumps(data).encode('utf-8')
#         await websocket.send(binary_data)

#         while True:
#             message = await websocket.recv()
#             decoded_data = decode_protobuf(message)
#             data_dict = MessageToDict(decoded_data)
#             print(json.dumps(data_dict))
#             await asyncio.sleep(2)  # Adjust sleep time as needed

# async def market_data(websocket, path):
#     while True:
#         data = await fetch_market_data()
#         await websocket.send(json.dumps(data))

# def start_websocket_server():
#     asyncio.set_event_loop(asyncio.new_event_loop())
#     loop = asyncio.get_event_loop()
#     server = websockets.serve(market_data, "localhost", 8765)
#     loop.run_until_complete(server)
#     loop.run_forever()

# threading.Thread(target=start_websocket_server, daemon=True).start()

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask,render_template,request
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')


@app.route('/home')
def main():
        return render_template('base.html')

@socketio.on("my_event")
def checkping():
    for x in range(5):
        cmd = 'ping -c 1 8.8.8.8|head -2|tail -1'
        listing1 = subprocess.run(cmd,stdout=subprocess.PIPE,text=True,shell=True)
        sid = request.sid
        emit('server', {"data1":x, "data":listing1.stdout}, room=sid)
        socketio.sleep(1)
