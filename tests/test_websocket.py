import websocket, requests, json
from lib_test import CabinSimulador
try:
    import thread
except ImportError:
    import _thread as thread
import time

#Parameters
IS_REMOTE = True
if IS_REMOTE:
    DOMAIN = '69.225.42.127'
    PORT = '3000'
    CABIN_TOKEN = 'uAo8DJ9ScE94Dk2a92U6vGCxw6R87GS0m9z371Za'
else:
    DOMAIN = 'localhost'
    PORT = '8000'
    CABIN_TOKEN = 'n8035q2xDpU1mH12zlb461V9W4g805o92H7R4P0h'
USER = {'username': 'test1', 'password': 'test_password'}
####
SERVER_URL_ALERT = 'ws://{}:{}/ws/alerts/'.format(DOMAIN,PORT)
SERVER_URL_AUTH = 'http://{}:{}/api/auth/login/'.format(DOMAIN,PORT)
SERVER_URL_CAPTURES = 'http://{}:{}/api/data/captures_create/'.format(DOMAIN,PORT)
####

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print('CONNECTED...')
        #Register captures
        simulator = CabinSimulador(SERVER_URL_CAPTURES, CABIN_TOKEN, verbose = False)
        for i in range(100):
            time.sleep(1)
            simulator.send_capture()
        time.sleep(1)
        ws.close()
        print("thread terminating...")
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
