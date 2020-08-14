import time
from lib_test import CabinSimulador

#Parameters
SERVER_URL = 'http://69.225.42.127:3000/api/data/captures_create/'
CABIN_TOKEN = 'QF11d735BL6J7OoJG5edc4mXXdRve206ze6Jx132'
SEND_TIME = 20 #Seconds between each request
#Simulator
simulator = CabinSimulador(SERVER_URL, CABIN_TOKEN, verbose = True)
#Show some info...
print('STARTING TEST FOR CABIN COMMUNICATION WITH SERVER...')
print('SENDING REQUESTS TO...{}\n'.format(SERVER_URL))
#Send data regularly
while True:
    simulator.send_capture()
    time.sleep(SEND_TIME)
