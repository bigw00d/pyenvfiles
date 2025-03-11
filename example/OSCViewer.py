import tkinter as tk
from tkinter import ttk

import sys
import os
from tkinter import *
from tkinter import messagebox,filedialog
# import numpy as np
from PIL import Image as pilimg
from PIL import ImageTk
import cv2

import pyvisa
import io

import threading
import time

# folder open & copy images
import subprocess
import glob
import shutil

# 注意：フォルダ名に日本語を含めないこと！

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()

        self.master.geometry("800x540")
        self.master.title("OSCViewer")

        self.create_widgets()

        self.img_cnt = 0
        self.print_cnt = 0
        self.view_idx = 0
        self.cdir = os.getcwd()
        self.fname = "Image" + str(self.img_cnt) + ".png"
        self.fpath = self.cdir + "\\" + self.fname
        self.cpydir = os.getcwd()
        print(self.fname)
        print(self.fpath)
        
        self.start = 0
        self.tf = 0
        self.routine10ms = 200
        self.tfcnt = 0

    def toggleStart(self):
        if self.start:
            self.start = 0
        else:
            self.start = 1
        self.updateOpeState(start=self.start)

    def stopRoutine(self):
        self.start = 0
        self.updateOpeState(start=self.start)

    def updateOpeState(self, start):
        if start:
            self.start = 1
            self.button_start.configure( text='Stop' )
            self.button_open2['state'] = tk.DISABLED
            self.button_open3['state'] = tk.DISABLED
            self.button_save2['state'] = tk.NORMAL
        else:
            self.start = 0
            self.button_start.configure( text='Start' )
            self.button_open2['state'] = tk.NORMAL
            self.button_open3['state'] = tk.NORMAL
            self.button_save2['state'] = tk.DISABLED

    def create_widgets(self):

        # Image Label
        self.device_label = ttk.Label(self)
        self.device_label.grid(column=1, row=0)
        self.device_label.configure(text = 'No Device')

        #Canvas
        self.canvas_width=640
        self.canvas_height=384
        self.canvas1 = tk.Canvas(self)
        self.canvas1.configure(width=self.canvas_width, height=self.canvas_height, bg='black')
        # self.canvas1.create_rectangle(0,0,120, 70, fill='green')
        # self.canvas1.grid(column=1, row=0)
        self.canvas1.grid(column=1, row=1)
        self.canvas1.grid(padx=20, pady=0)

        # Right Frame
        self.frame_right = ttk.LabelFrame(self)
        self.frame_right.configure(text=' Operation ')
        self.frame_right.grid(column=2,row=1)

        # Start Button
        self.button_start = ttk.Button( self.frame_right )
        self.button_start.configure( text='Start' )
        self.button_start.grid( column=0, row=1 )
        self.button_start.configure(command=self.toggleStart)
        self.button_start.grid(padx=0, pady=5)

        # Save Button
        self.button_save2 = ttk.Button( self.frame_right )
        self.button_save2.configure( text='Save' )
        self.button_save2.grid( column=0, row=2 )
        self.button_save2.configure(command=self.saveImage)
        self.button_save2.grid(padx=0, pady=5)
        self.button_save2['state'] = tk.DISABLED

        # Copy Button
        self.button_copy = ttk.Button( self.frame_right )
        self.button_copy.config( text='CopyAll' )
        self.button_copy.grid( column=0, row=3 )
        self.button_copy.configure(command = self.copyImage)
        self.button_copy.grid(padx=0, pady=5)

        # Open Button
        self.button_open = ttk.Button( self.frame_right )
        self.button_open.config( text='Open' )
        self.button_open.grid( column=0, row=4 )
        self.button_open.configure(command = self.openImage)
        self.button_open.grid(padx=0, pady=5)

        # Quit Button
        self.button_quit = ttk.Button( self.frame_right )
        self.button_quit.config( text='Quit' )
        self.button_quit.grid( column=0, row=5 )
        self.button_quit.configure(command = self.quit_app)

        # # Image Label
        # self.save_label = ttk.Label( self.frame_right )
        # self.save_label.grid(column=0, row=3)
        # self.save_label.configure(text = 'No Image')

        # Image Label
        self.image_label = ttk.Label(self)
        self.image_label.grid(column=1, row=2)
        self.image_label.configure(text = 'No Image')

        #Frame
        self.frame_button = ttk.LabelFrame(self)
        self.frame_button.configure(text=' View Menu ')
        self.frame_button.grid(column=1,row=3)
        self.frame_button.grid(padx=20, pady=20)

        # # # Load Image
        # # Select Folder
        # self.button_open = ttk.Button(self.frame_button)
        # # self.button_open.configure(text = 'Print Screen')
        # self.button_open.configure(text = 'Select Folder')
        # self.button_open.grid(column=0, row=1)
        # # self.button_open.configure(command=self.loadImage)
        # self.button_open.configure(command=self.openFolder)

        # # # Save Button
        # # self.button_save = ttk.Button( self.frame_button )
        # # self.button_save.configure( text='Save Image' )
        # # self.button_save.grid( column=1, row=1 )
        # # self.button_save.configure(command=self.saveImage)

        # # Quit Button
        # self.button_quit = ttk.Button( self.frame_button )
        # self.button_quit.config( text='Quit' )
        # self.button_quit.grid( column=2, row=1 )
        # self.button_quit.configure(command = self.quit_app)

        # #Folder Path
        # self.folder_path = ttk.Entry(self.frame_button)
        # self.folder_path.insert(tk.END, ".\\")
        # self.folder_path.grid(column=0, row=2, columnspan=3, padx=20, ipadx=50)
        # self.folder_path.configure(state='readonly')

        #File open and Load Image
        self.button_open2 = ttk.Button(self.frame_button)
        self.button_open2.configure(text = ' << ')
        self.button_open2.grid(column=0, row=3)
        self.button_open2.configure(command=self.viewFileL)

        # Image Label
        self.index_label = ttk.Label(self.frame_button)
        self.index_label.grid(column=1, row=3)
        self.index_label.configure(text = ' -- ')
        self.index_label.grid(padx=40, pady=0)

        #File open and Load Image
        self.button_open3 = ttk.Button(self.frame_button)
        self.button_open3.configure(text = ' >> ')
        self.button_open3.grid(column=2, row=3)
        self.button_open3.configure(command=self.viewFileR)

    # Event Call Back
    def openFolder(self):
        self.cdir = filedialog.askdirectory()
        print(self.cdir)
        self.folder_path.configure(state='normal')
        self.folder_path.delete(0,tk.END)
        self.folder_path.insert(tk.END, "%s" % self.cdir)
        self.folder_path.configure(state='readonly')

    def loadImage(self):

        print('loadImage')
        rm = pyvisa.ResourceManager()
        visa_list = rm.list_resources()
        usb_list = [i for i in visa_list if 'USB' in i] # "USB0::0x....."のようなメンバ(USB VISA機器)を抽出する 

        if len(usb_list) > 0:
            usb_1 = usb_list[0]
            inst_1 = rm.open_resource(usb_1)

            out = inst_1.query('*IDN?')
            # out: <device id>,<model>,<serial number>,<software version>,<hardware version> 
            print(out)
            # self.device_label.configure(text = out)
            infolist = out.split(',')
            if len(infolist) > 2:
                model = infolist[1]
                self.device_label.configure(text = "model: " + model)

            bmp_bin = inst_1.query_binary_values(':DISP:DATA?', datatype='B', container=bytes)
            self.img = pilimg.open(io.BytesIO(bmp_bin)) # get PIL image
            w = self.img.width # 横幅を取得
            h = self.img.height # 縦幅を取得 
            print("w, h = " + str(w)+ "," + str(h))
            self.new_size = (self.canvas_width,self.canvas_height)
            # prtimg = self.img.resize(self.new_size, resample=pilimg.NEAREST)
            prtimg = self.img.resize(self.new_size, resample=pilimg.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(prtimg) # PIL image -> TK image
            self.canvas1.create_image(self.canvas_width/2,self.canvas_height/2, image=self.image_tk)
            self.print_cnt = 1
            self.view_idx = self.img_cnt + 1
            self.image_label.configure(text = 'New Image')
            indextxt = "-- / " + str(self.img_cnt)
            self.index_label.configure(text = indextxt)
            # self.index_label.configure(text = ' -- ')
            print("display screen")
        else:
            print("no device")
            tk.messagebox.showinfo("Info", "failure: no connected devices found")
            self.stopRoutine()

    def viewFile(self):

        print('viewFile')
        # self.filename = filedialog.askopenfilename()
        # print(self.filename)
        self.fname = "Image" + str(self.view_idx) + ".png"
        self.fpath = self.cdir + "\\" + self.fname
        print("self.fname: " + self.fname)
        print("self.fpath: " + self.fpath)
        self.image_label.configure(text = self.fname)
        indextxt = str(self.view_idx) + " / " + str(self.img_cnt)
        self.index_label.configure(text = indextxt)

        self.image_PIL = pilimg.open(self.fpath) # PILフォーマットで開く
        self.resize_PIL = self.image_PIL.resize((self.canvas_width,self.canvas_height))
        self.image_tk = ImageTk.PhotoImage(self.resize_PIL) # ImageTkフォーマットへ変換
        self.canvas1.create_image(self.canvas_width/2,self.canvas_height/2, image=self.image_tk)
        print("view image")


    def viewFileL(self):

        print('viewFileL')

        if self.view_idx > 1:
            # self.filename = filedialog.askopenfilename()
            # print(self.filename)

            self.view_idx-=1
            self.viewFile()
        else:
            tk.messagebox.showinfo("Info", "no image")

    def viewFileR(self):

        print('viewFileR')

        if self.view_idx < self.img_cnt:

            self.view_idx+=1
            self.viewFile()
        else:
            tk.messagebox.showinfo("Info", "no image")

    def openImage(self):
        subprocess.Popen(["explorer", self.cdir], shell=True)

    def copyImage(self):
        # tk.messagebox.showinfo("Info", "no image")
        self.cpydir = filedialog.askdirectory()
        print(self.cpydir)
        image_path = self.cdir + '\\Image' + '*' + '.png'
        print("image_path: " + image_path)
        files = glob.glob(image_path)
        print("copy start")
        print(files)
        cpyOk = True
        for file in files:
            print(file)
            try:
                new_file_path = file.replace(self.cdir, self.cpydir)
                shutil.copy(file, new_file_path)
                print("-> copy ok: " + new_file_path)
            except FileNotFoundError:
                print("-> FileNotFoundError: " + new_file_path)
                cpyOk = False
                pass
            except OSError:
                print("-> OSError: " + new_file_path)
                cpyOk = False
                pass
        if cpyOk:
            tk.messagebox.showinfo("Info", "success")
        else:
            tk.messagebox.showinfo("Info", "error")

    def saveImage(self):

        if self.print_cnt > 0:
            self.print_cnt = 0
            self.img_cnt+=1
            self.view_idx = self.img_cnt
            self.fname = "Image" + str(self.img_cnt) + ".png"
            self.fpath = self.cdir + "\\" + self.fname
            self.img.save(self.fpath,"PNG")
            self.image_label.configure(text = self.fname)
            indextxt = "-- / " + str(self.img_cnt)
            self.index_label.configure(text = indextxt)
            # tk.messagebox.showinfo("Info", "success: Saved " + self.fname)
            # self.save_label.configure(text = self.fname)
        else:
            tk.messagebox.showinfo("Info", "no image")
    
    def quit_app(self):
        self.Msgbox = tk.messagebox.askquestion("Exit Applictaion", "Are you sure?", icon="warning")
        if self.Msgbox == "yes":
            # self.master.destroy()
            self.on_closing()
        else:
            tk.messagebox.showinfo("Return", "you will now return to application screen")

    def comm_worker(self):
        print('comm_worker start')
        self.tf = 1 # tf=1 -> enable therad roop
        while self.tf:
            self.tfcnt+=1
            if self.tfcnt >= self.routine10ms:
                self.tfcnt = 0
                if self.start:
                    self.loadImage()
                print('comm_worker')
            time.sleep(0.001) # 注意：精度が10msレベルであまり正確でない
            # time.sleep(2.000)
            # print('comm_worker')

    def on_closing(self):
        self.tf = 0
        self.master.destroy()

def main():
    # print(cv2.path)
    root = tk.Tk()
    app = Application(master=root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    threadComm = threading.Thread(target=app.comm_worker)
    threadComm.start()
    app.mainloop()

if __name__ == "__main__":
    main()

