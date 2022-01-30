# URL for test: https://youtu.be/9MpO8lw_Rj4
import os
import re
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory
import tkinter.ttk as ttk
from error_handler import ErrorHandler
from downloader import AudioDownloader

folder = os.getcwd()
err_handler=ErrorHandler(folder)
downloader=AudioDownloader(err_handler)

# GUI
window=Tk()
window.title('Audio Downloader')
window.iconbitmap("./icon.ico")

title_fontstyle=tkFont.Font(family='Arial',size=16)
utility_fontstyle=tkFont.Font(family='Arial',size=12)
queue_fontstyle=tkFont.Font(family='Ubuntu Light',size=12)

path=StringVar()
URLs=StringVar()

title=Label(window,text="Audio Downloader",font=title_fontstyle)
title.pack(side=TOP)

# URLs input
URL_frame=Frame(window)
URL_frame.pack(side=TOP,pady=40)
URL_label=Label(URL_frame,text="Youtube URL: ",font=utility_fontstyle)
URL_entry=Entry(URL_frame,width=80,font=utility_fontstyle)
def render_queue(e=None):
    if "Errors occur. See ./Err_Msg.txt" in board.get("0.0",END):
        board.delete('0.0',END)
    new_url= re.sub(" ","", URL_entry.get())
    valid=downloader.append_URL(new_url)
    if valid:
        yt=downloader.get_yt_objects()[-1]
        idx=len(downloader.get_yt_objects())
        board.insert('insert',"["+str(idx)+"]"+yt.title+"\n\n")
        board.yview_pickplace('end')
    else:
        messagebox.showerror("Invalid Youtube URL","[Invalid Youtube URL]   "+URL_entry.get())
    URL_entry.delete(0,'end')
URL_btn=Button(URL_frame,text='+',font=utility_fontstyle,command=render_queue)

URL_label.pack(side=LEFT)
URL_entry.pack(side=LEFT)
URL_btn.pack(side=LEFT)

board=ScrolledText(window,wrap=WORD,width=100,height=12,bg='black',fg='white',font=queue_fontstyle)
board.pack()
window.bind('<Return>',render_queue)

# config frame
def select_dir():
    path_=askdirectory()
    path.set(path_)

config_frame=Frame(window,pady=4)
config_frame.pack(side=TOP)

path_frame=Frame(config_frame)
path_frame.pack(side=TOP)
path_label=Label(path_frame,text="Destination: ",font=utility_fontstyle)
path_entry=Entry(path_frame,textvariable=path,width=60,font=utility_fontstyle)
path_btn=Button(path_frame,command=select_dir,text="Search",font=utility_fontstyle)
path_entry.insert(0,os.getcwd())
path_label.pack(side=LEFT)
path_entry.pack(side=LEFT)
path_btn.pack(side=LEFT)

format_frame=Frame(config_frame)
format_frame.pack(side=LEFT)
format_label=Label(format_frame,text="Audio format: ",font=utility_fontstyle)
format_combo=ttk.Combobox(format_frame,value=["wav","mp3","m4a","mp4"],state='readonly',width=6,font=utility_fontstyle)
format_combo.current(0)
format_label.pack(side=LEFT)
format_combo.pack(side=LEFT)

normalize_frame=Frame(config_frame)
normalize_frame.pack(side=RIGHT)
def normalize_validate(p):
    if  str.isdigit(p.lstrip('-')) or (p == "-"):
        return True
    return False
valid_cmd=(config_frame.register(normalize_validate),"%S")
normalize_label1=Label(normalize_frame,text="Normalize to ",font=utility_fontstyle)
normalize_entry=Entry(normalize_frame,validate='key',width=6,validatecommand=valid_cmd,font=utility_fontstyle,)
normalize_label2=Label(normalize_frame,text=" dBFS",font=utility_fontstyle)
normalize_entry.insert(0,"-6")
normalize_label1.pack(side=LEFT)
normalize_entry.pack(side=LEFT)
normalize_label2.pack(side=LEFT)

# START button
def start_convert():
    dir_path=str(path_entry.get())
    dBFS=int(normalize_entry.get().lstrip('-'))
    if normalize_entry.get()[0]=='-':
        dBFS=dBFS*(-1)
    if not os.path.isdir(dir_path):
        messagebox.showerror("Destination path not found","path "+dir_path+" doesn't exists.")
        return False
    downloader.set_dir(path_entry.get())
    downloader.set_Format(format_combo.get())
    downloader.set_dBFS(dBFS)
    perfect=downloader.convert()
    if perfect:
        board.delete('0.0',END)
    else:
        board.insert('insert',"\n\n Errors occur. See ./Err_Msg.txt\n")
    return perfect
start_frame=Frame(window,width=100,pady=40)
start_frame.pack()
start_btn=Button(start_frame,width=80,text='Convert',bg='white',command=start_convert,font=utility_fontstyle)
start_btn.pack(side=LEFT)

window.mainloop()