#!usr/bin/python3 #TODO make desktop launcher
#include gps data support

from tkinter import *
import threading
import queue
import socket
from tkinter import messagebox
import datetime

class myCFred(threading.Thread): #searches acc and coo
    def __init__(self, coordinates_Queue):
        threading.Thread.__init__(self)
        self.stoprequest = threading.Event()
        self.coordinates_Queue = coordinates_Queue

    def run(self):
        UDP_IP = "10.0.24.199"
        Port = 5006
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, Port))

        while 1:
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8") #EXTRACT INFORMATION TODO
            self.coordinates_Queue.put(data)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(myCFred, self).join(timeout)



class myFred (threading.Thread):
    def __init__ (self, msg_Queue, data_Queue):
        threading.Thread.__init__(self)
        self.data_Queue = data_Queue
        self.msg_Queue = msg_Queue
        self.stoprequest = threading.Event()

    def run(self):
        UDP_IP = "10.0.24.199"
        Port = 5005
  
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, Port))

        while 1:
            data, addr = sock.recvfrom(1024)
            data = data.decode("utf-8")

            if data.startswith("PACKAGE"):
                self.msg_Queue.put(1)
            elif data.startswith("ACCELERATION"):
                self.msg_Queue.put(2)
            else:
                self.data_Queue.put(data)

    def join(self, timeout=None):
        self.stoprequest.set()
        super(myFred, self).join(timeout)



def main():
    root = Tk()
    root.title("SenseTracker")

    t = Label(root, text = "")
    b1 = Label(root, text = "")
    b2 = Label(root, text = "")
    w = Label(root, text = "All Devices Okay")
    w.config(font=("Arial", 44)) 
    t.config(font=("Arial", 44)) 
    b1.config(font=("Arial", 20)) 
    b2.config(font=("Arial", 20)) 
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
    data_Queue = queue.Queue()
    t1 = myFred(msg_Queue, data_Queue)
    t1.start()

    coordinates_Queue = queue.Queue()
    t2 = myCFred( coordinates_Queue)
    t2.start()

    data = " "
    coo = "(-1, -1)"
    corrupt_flag = False

    while 1:
        try: 
            msg = msg_Queue.get(False) #is there an acc-interrupt? 
            if msg == 1:
                corrupt_flag = True
                w.config(text= "PACKAGE OPENED", font=("Arial", 44)) 
                root.update()
                messagebox.showerror("PACKAGE OPENED SIGNAL", \
                        "The package was opened. Please check the coordinates and track your parcel")
                w.config(text= "Parcel was opened!", font=("Arial", 44)) 
                b2.config(text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                root.update()
            elif msg == 2:
                #act
                corrupt_flag = True
                w.config(text= "PACKAGE DROPED", font=("Arial", 44)) 
                root.update()
                messagebox.showerror("PACKAGE DROPED", \
                        "The package was droped. Please check the coordinates and track your parcel")
                w.config(text= "Parcel was droped!", font=("Arial", 44)) 
                b2.config(text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                root.update()
            with data_Queue.mutex:
                data_Queue.queue.clear()
            with msg_Queue.mutex:
                msg_Queue.queue.clear()

        except queue.Empty: #no there is no interrupt
            try:
                data = str(data_Queue.get(False))
            except queue.Empty: #no there is no opening interrupt and also no acc-interrupt
                pass
        status.config(text=data)
        root.update()
        print (data)

        if corrupt_flag == True:
            try: 
                coo = str(coordinates_Queue.get(False))
            except queue.Empty:
                pass
            b1.config(text = "Location: " + coo) 
            root.update()


if __name__ == "__main__":
    main()
