# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import time
import pycom
import math

def main():

    py = Pysense()
    mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    si = SI7006A20(py)
    lt = LTR329ALS01(py)
    li = LIS2HH12(py)

    pycom.heartbeat(0)
    pycom.rgbled(0x0f0000)
    max_x = 0
    max_y = 0
    max_z = 0
    while 1:

        #print("MPL3115A2 temperature: " + str(mp.temperature()))
        #print("Altitude: " + str(mp.altitude()))
        #mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
        #print("Pressure: " + str(mpp.pressure()))

        #print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
        #print("Dew point: "+ str(si.dew_point()) + " deg C")
        #t_ambient = 24.4
        #print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

        #print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))
        acc = li.acceleration()
        if abs(acc[0]) > abs(max_x):
            max_x = acc[0]
        if abs(acc[1]) > abs(max_y):
            max_y = acc[1]
        if abs(acc[2]) > abs(max_z):
            max_z = acc[2]
        max_str = "max: ({:1.3f}, {:1.3f}, {:1.3f})".format(max_x, max_y, max_z)
        print("Acceleration: " + str(acc)+ " " + max_str)
        #print("Roll: " + str(li.roll()))
        #print("Pitch: " + str(li.pitch()))

        #print("Battery voltage: " + str(py.read_battery_vpoltage()))
        time.sleep(0.2)
if __name__ == '__main__':
    main()
