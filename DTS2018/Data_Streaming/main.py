# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from network import WLAN
import time
import pycom
import math
import socket
import time
import machine

def main():
    pycom.heartbeat(0)
    debug_flag = False

    #Init sensors
    py = Pysense()
    mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    #si = SI7006A20(py)
    lt = LTR329ALS01(py)
    li = LIS2HH12(py)

    #Init WLAN connection
    wlan = WLAN(mode=WLAN.STA)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == 'gotechsummit':
            if debug_flag == True:
                print('Network found!') #debugging
            wlan.connect(net.ssid, auth=(net.sec, 'HackTime247'), timeout=5000)
            while not wlan.isconnected():
                machine.idle() #to save energy
            if debug_flag == True:
                print ("Connection Successful") #debug
            break

    #Init the UDP transmission
    UDP_IP_Josch = "10.0.24.199"
    UDP_IP_Niklas = "10.0.25.80"
    UDP_IP_Ulrich = "10.0.25.173"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    counter = 0


    while 1:
        #temperature = mp.temperature()
        #temperature_2 = si.temperature()
        light = lt.light()
        acceleration = li.acceleration()
        battery = py.read_battery_voltage()

        a_vector = (acceleration[0]**2) + (acceleration[1]**2) + (acceleration[2]**2)
        l_vector = (light[0]**2) + (light[1]**2)

        if a_vector > 3:
            MESSAGE = "ACCELERATION INTERRUPT"
        elif l_vector > 3:
            MESSAGE = "PACKAGE OPENING INTERRUPT"
        else:
            MESSAGE = str(counter) + ";" + str(light) + ";" + \
                str(acceleration) + ";" + str(battery)
                
        sock.sendto(MESSAGE, (UDP_IP_Josch, UDP_PORT))
        #sock.sendto(MESSAGE, (UDP_IP_Niklas, UDP_PORT))
        #sock.sendto(MESSAGE, (UDP_IP_Ulrich, UDP_PORT))
        if debug_flag == True:
            #print ("Temperature:   " + str(temperature))
            #print ("Temperature_2: " + str(temperature_2))
            print ("Light:         " + str(light))
            print ("Accerlation:   " + str(acceleration))
            print ("Battery:       " + str(battery))
            print("Successfully Sent Package #" + str(counter))
            print("\n\n\n")
        counter = counter + 1
        if debug_flag == True:
            for i in range(0,4):
                pycom.rgbled(0x00ff00)
                time.sleep(0.2)
                pycom.rgbled(0xff0000)
                time.sleep(0.2)
        else:
            time.sleep(0.05)
if __name__ == '__main__':
    main()
