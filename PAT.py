# -*- coding: utf-8 -*-
#!/home/noselab/anaconda3/envs/Canon2/bin python3.6
import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import TP

def button1_clicked():
    fTyp = [("","*.tif")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    file1.set(filepath)

def button5_clicked():
    flag=False
    if file1.get().split("/")[-1].split(".")[0]=="":
        messagebox.showinfo('Error','This tif file is hidden file or something wrong. Please check it.')
        return
    try:
        int(number_entry.get())
    except:
        messagebox.showinfo('Error','Input number (point) is incorrect. Even number is required. Please check it.')
        return
    
    if int(number_entry.get())%2!=0:
        messagebox.showinfo('Error','Input number (point) is incorrect. Even number is required. Please check it.')
        return
    elif int(number_entry.get())<2:
        messagebox.showinfo('Error','Input number (point) is incorrect. Even number is required. Please check it.')
        return
    else:
        pass
    
    try:
        int(number21_entry.get())
    except:
        messagebox.showinfo('Error','Input number (initial flame) is incorrect. Please check it.')
        return
    
    try:
        int(number22_entry.get())
    except:
        messagebox.showinfo('Error','Input number (final flame) is incorrect. Please check it.')
        return
    TP.twopoints(file1.get(),int(number_entry.get()),int(number21_entry.get()),int(number22_entry.get()))
    
def button52_clicked():
    file1_entry.delete(0, END)
    number_entry.delete(0, END)
    number21_entry.delete(0, END)
    number22_entry.delete(0, END)

def quits():
    sys.exit()
    
if __name__ == '__main__':
    
    root = Tk()
    root.title('Annotation tool')
    root.resizable(False, False)
   
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid()

    button1 = ttk.Button(root, text='Browse', command=button1_clicked)
    button1.grid(row=0, column=3)

    s = StringVar()
    s.set('Select a file to open >>')
    label1 = ttk.Label(frame1, textvariable=s)
    label1.grid(row=0, column=0)

    file1 = StringVar()
    file1_entry = ttk.Entry(frame1, textvariable=file1, width=50)
    file1_entry.grid(row=0, column=2)
    
    frame2 = ttk.Frame(root)
    frame2.grid()
    
    label2 = ttk.Label(frame2, text='input number of points >>')
    label2.grid(row=0, column=0)
    number_entry = ttk.Entry(frame2,width=5)
    number_entry.grid(row=0, column=1)
    
    label21 = ttk.Label(frame2, text='input number of initial frame >>')
    label21.grid(row=1, column=0)
    number21_entry = ttk.Entry(frame2,width=5)
    number21_entry.grid(row=1, column=1)
    
    label22 = ttk.Label(frame2, text='input number of final frame >>')
    label22.grid(row=2, column=0)
    number22_entry = ttk.Entry(frame2,width=5)
    number22_entry.grid(row=2, column=1)
    
    frame5 = ttk.Frame(root, padding=(0,5))
    frame5.grid()

    button5 = ttk.Button(frame5, text='Start', command=button5_clicked)
    button5.pack(side=LEFT)

    button52 = ttk.Button(frame5, text='Clear', command=button52_clicked)
    button52.pack(side=LEFT)
    
    button51 = ttk.Button(frame5, text='Cancel', command=quits)
    button51.pack(side=LEFT)

    root.mainloop()