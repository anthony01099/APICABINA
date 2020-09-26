import websocket, requests, json
from lib_test import CabinSimulador
try:
    import thread
except ImportError:
    import _thread as thread
import time


DOMAIN = 'localhost'
PORT = '3000'
CABIN_TOKEN = 'n8035q2xDpU1mH12zlb461V9W4g805o92H7R4P0h'
USER = {'username': 'test1', 'password': 'test_password'}
####
SERVER_URL_ALERT = 'ws://{}:{}/api/booth_messages/{}/'.format(DOMAIN,PORT,CABIN_TOKEN)
SERVER_URL_AUTH = 'http://{}:{}/api/auth/login/'.format(DOMAIN,PORT)
SERVER_URL_CAPTURES = 'http://{}:{}/api/data/captures_create/'.format(DOMAIN,PORT)

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print('CONNECTED...')
    thread.start_new_thread(run, ())

def get_auth_credentials():
    response = requests.post(SERVER_URL_AUTH, data = json.dumps(USER))
    txt = 'csrftoken={}; sessionid={}'.format(response.cookies['csrftoken'],response.cookies['sessionid'])
    return txt

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_URL_ALERT,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie = get_auth_credentials())
    ws.on_open = on_open
    ws.run_forever()
