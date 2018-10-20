import socket
from network import WLAN
import time
import pycom
import machine


pycom.heartbeat(0)
wlan = WLAN(mode=WLAN.STA)
#login to wifi
nets = wlan.scan()
for net in nets:
    if net.ssid == 'gotechsummit':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'HackTime247'), timeout=5000)
        while not wlan.isconnected():
            machine.idle()
        print ("Connection Successful")
        break

UDP_IP_Josch = "10.0.24.199"
UDP_IP_Niklas = "10.0.25.80"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MESSAGE = "Hello World, Motherfucker!"
counter = 0
while 1:
    sock.sendto(MESSAGE, (UDP_IP_Josch, UDP_PORT))
    sock.sendto(MESSAGE, (UDP_IP_Niklas, UDP_PORT))
    print("Successfully Sent Package #" + str(counter))
    counter = counter + 1
    for i in range(0,4):
        pycom.rgbled(0x00ff00)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.5)
