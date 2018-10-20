#!usr/bin/python3 #TODO make desktop launcher

from tkinter import *
import threading
import queue
import socket
from tkinter import messagebox

class myFred (threading.Thread):
    def __init__ (self, msg_Queue, coordinates_Queue, data_Queue):
        threading.Thread.__init__(self)
        self.msg_Queue = msg_Queue
        self.coordinates_Queue = coordinates_Queue
        self.data_Queue = data_Queue
        self.stoprequest = threading.Event()

    def run(self):
        UDP_IP = "10.0.24.199"
        Port = 5005
  
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, Port))
        #gps_data_x = ---
        #gps_data_y = --

        while 1:
            #if gps_update_available:
            # update gps_data_x, gps_data_y
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8")
            if data.startswith("PACKAGE"):
                self.msg_Queue.put(1)
                #print gps_data_x
            elif data.startswith("ACCELERATION"): #
                #print gps_data_x
                self.msg_Queue.put(2)
            else:
                self.data_Queue.put(data)


    def join(self, timeout=None):
        self.stoprequest.set()
        super(myFred, self).join(timeout)

def main():
    root = Tk()
    root.title("SenseTracker")
    data = ""
    coo = (-1,-1)

    t = Label(root, text = "")
    b1 = Label(root, text = "")
    b2 = Label(root, text = "")
    w = Label(root, text = "All Devices Okay")
    w.config(font=("Arial", 44)) 
    t.config(font=("Arial", 44)) 
    b1.config(font=("Arial", 20)) 
    b2.config(font=("Arial", 50)) 
    t.config(font=("Arial", 44)) 
    w.config(width=30)
    t.pack()
    w.pack()
    b1.pack()
    b2.pack()

    status = Label(root, text="Active Device at Mac Adress 30:ae:a4:79:00:0c ...", bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    root.update()

    #create queue for the thread
    msg_Queue = queue.Queue()
    coordinates_Queue = queue.Queue()
    data_Queue = queue.Queue()
    #create thread that monitors the udp package intake
    t1 = myFred(msg_Queue, coordinates_Queue, data_Queue)
    t1.start()

    while 1: #gui loop
        try:
            val = msg_Queue.get(False)
            try:
                coo = coordinates_Queue.get(False)
            except queue.Empty:
                pass
            if val ==1:
                w.config(text= "PACKAGE INTERRUPT", font=("Arial", 44)) 
                b1.config(text = "Long: "+ str(coo[0]) + "          Lat: " + str(coo[1])) #add time TODO
                root.update()
                messagebox.showerror("Package INTERRUPT", \
                        "The package was opened. Please check the coordinates and track your parcel")
                w.config(text= "Devices might be corrupted", font=("Arial", 44)) 
                root.update()
                with msg_Queue.mutex:
                    msg_Queue.queue.clear()
                with data_Queue.mutex:
                    data_Queue.queue.clear()
            if val == 2:
                w.config(text= "ACCELERATION INTERRUPT", font=("Arial", 44)) 
                b1.config(text = "Long: "+ str(coo[0]) + "          Lat: " + str(coo[1])) #add time TODO
                root.update()
                messagebox.showerror("Acceleration INTERRUPT", \
                        "The package was droped. Please check the coordinates and track your parcel")
                w.config(text= "Devices might be corrupted", font=("Arial", 44)) 
                root.update()
                with msg_Queue.mutex:
                    msg_Queue.queue.clear()
                with data_Queue.mutex:
                    data_Queue.queue.clear()
        except queue.Empty: #Queue empty = no interrupts
            try:
                data = data_Queue.get(False)
            except queue.Empty:
                pass
            print(data + 30*" ", end="\r", flush = True)

if __name__ == "__main__":
    main()
