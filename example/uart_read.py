import tkinter as tk
import tkinter.scrolledtext
import time

from time import sleep
from tkinter import ttk
from tkinter import messagebox

import serial
from serial.tools import list_ports

import threading

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()

        self.master.geometry('530x160')
        self.master.title("Uart Sample")

        self.create_widgets()

        self._serial = serial.Serial()
        # self._serial=''
        self.com_open = 0

    def create_widgets(self):
        self.label1 = tk.Label(self, text = 'Device List : ')
        self.label1.grid(row=0, column=0)
        self.label2 = tk.Label(self,text = 'Serial Baud :' )
        self.label2.grid(row=1, column=0)
        self.cbDevList= ttk.Combobox(self , width=50 )
        self.cbDevList.grid(row=0 , column=1)
        self.cbDevList.bind('<<ComboboxSelected>>',self.cmb_Sel)
        self.txtOption = ttk.Entry(self , width=50 , state =tk.DISABLED )
        self.txtOption.grid(row=1 , column=1)
        self.txtSend = ttk.Entry(self , width=50 )
        self.txtSend.grid(row=2 , column=1)
        self.txtSend.insert(tk.END,'*idn?')
        self.txtRecive = tk.Text(self , width=42, height=5 )
        self.txtRecive.grid(row=3 , column=1)
        self.btn1 = tk.Button(master=self, text=' Find ' , command=self.Find_clicked)
        self.btn1.grid(row = 0 , column=2)
        self.btn2 = tk.Button(master=self, text=' Exit ' , command=self.Exit_clicked)
        self.btn2.grid(row = 0 , column=3)
        self.btn3 = tk.Button(master=self, text=' Open ' , command=self.Open_clicked, state =tk.DISABLED )
        self.btn3.grid(row = 1 , column=2)
        self.btn4 = tk.Button(master=self, text=' Close ' , command=self.Close_clicked, state =tk.DISABLED )
        self.btn4.grid(row = 1 , column=3)
        self.btn5 = tk.Button(master=self, text=' Send ' , command=self.Send_clicked, state =tk.DISABLED )
        self.btn5.grid(row = 2 , column=0)
        self.btn6 = tk.Button(master=self, text=' Recive ' , command=self.Recive_clicked, state =tk.DISABLED )
        self.btn6.grid(row = 3 , column=0)

    def cmb_Sel(self, event):
        self.txtOption.delete(0,tk.END)
        # cbDevList['values']=['']
        # cbuff = cbDevList.get()
        # if('ASRL' in cbuff):
        #     self.txtOption['state'] = tk.NORMAL
        #     self.txtOption.insert(tk.END,'115200')
        # else:
        #     self.txtOption['state'] = tk.DISABLED

    def Find_clicked(self):
        print('Find_clicked')
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports]
        if len(port_names) > 0:
            self.cbDevList.configure(values=port_names)
            self.cbDevList.set(port_names[0])
            self.btn3['state'] = tk.NORMAL
        else:
            port_names=[]
            self.cbDevList.configure(values=port_names)
            self.cbDevList.set('')
            self.btn3['state'] = tk.DISABLED
            print('Device Error')

    def Exit_clicked(self):
        print('Exit_clicked')
        self.Msgbox = tk.messagebox.askquestion("Exit Applictaion", "Are you sure?", icon="warning")
        if self.Msgbox == "yes":
            # self.master.destroy()
            self.on_closing()
        else:
            tk.messagebox.showinfo("Return", "you will now return to application screen")

    def Open_clicked(self):
        print('Open_clicked')
        try:
            self._serial = serial.Serial()
            # self._serial.port = 'COM8' # 'COM' + txtPort.get()
            self._serial.port = self.cbDevList.get()            
            self._serial.baudrate = 38400     # ボーレート指定
            self._serial.parity = serial.PARITY_NONE
            self._serial.bytesize = serial.EIGHTBITS
            self._serial.stopbits = serial.STOPBITS_TWO
            self._serial.timeout = 0.040      # タイムアウト指定(40ms)
            self._serial.open()
            self.com_open = 1
            sleep(0.1)
            self.txtRecive.insert(tk.END,'open: %s\n' % self.cbDevList.get())
            # self.txtRecive.insert(tk.END,'open: COM8\n')
            self.btn3['state'] = tk.DISABLED       # Open
            self.btn4['state'] = tk.NORMAL       # Close
            self.btn6['state'] = tk.DISABLED     # Recive

        except:
            # self.txtRecive.insert(tk.END,'cannot open\n')
            self.txtRecive.insert(tk.END,'cannot open: %s\n' % self.cbDevList.get())
            self.Close_clicked()

    def Close_clicked(self):
        print('Close_clicked')
        self.com_open = 0
        self._serial.close()
        self.btn3['state'] = tk.NORMAL       # Open
        self.btn4['state'] = tk.DISABLED       # Close
        self.btn6['state'] = tk.DISABLED     # Recive
        self.txtRecive.insert(tk.END,'close\n')

    def Send_clicked(self):
        print('Send_clicked')

    def Recive_clicked(self):
        print('Recive_clicked')

    def comm_worker(self):
        print('comm_worker start')
        self.tf = 1 # tf=1 -> enable therad roop
        while self.tf:
            # print('comm_worker')
            if self.com_open:
                data=self._serial.readline()
                # data=data.strip()
                try:
                    data=data.decode('utf-8')
                    # data=data.decode('sjis')
                    if data :
                        print(data, end='')
                        self.txtRecive.insert(tk.END,'%s' % data)
                        self.txtRecive.see('end')
                except:
                    print('cannot decode')
            time.sleep(0.001) # 注意：精度が10msレベルであまり正確でない
            # time.sleep(1.001) # 注意：精度が10msレベルであまり正確でない

    def on_closing(self):
        self.tf = 0
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Application(master=root)#Inherit
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    thread = threading.Thread(target=app.comm_worker)
    thread.start()
    app.mainloop()

if __name__ == "__main__":
    main()

