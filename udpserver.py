import socket 
from tkinter import messagebox
import time

def main():

    UDP_IP = "10.0.24.199"
    Port = 5006

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, Port))
    #gps_data_x = ---
    #gps_data_y = -- 

    while 1:
            #if gps_update_available:
            # update gps_data_x, gps_data_y
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8")
            print (data)
            continue
            if data.startswith("PACKAGE"):
                    print("PACKAGE OPENING INTERRUPT DETECTED" + 30*" " , \
                            end = "\r", flush = True)
                    #print gps_data_x
            elif data.startswith("ACCELERATION"): #
                    print("ACCELERATION INTERRUPT DETECTED " + 30*" "  , \
                            end = "\r", flush = True)
                    #print gps_data_x
                    time.sleep(3)
            else:
                    print (data + 30*" ", end="\r", flush = True)
if __name__ == "__main__":
	main()























