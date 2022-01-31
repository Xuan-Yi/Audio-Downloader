import os
import re
from pytube import YouTube
from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import askdirectory
import tkinter.ttk as ttk
from cores.downloader import AudioDownloader
from components.board import Board

folder = os.getcwd()
downloader=AudioDownloader()

# GUI
window=Tk()
window.title('Audio Downloader')
window.iconbitmap("./images/icon.ico")

title_fontstyle=tkFont.Font(family='Arial',size=16)
utility_fontstyle=tkFont.Font(family='Arial',size=12)
queue_fontstyle=tkFont.Font(family='Ubuntu Light',size=12)

path=StringVar(value=os.getcwd())
URLs=StringVar()

title=Label(window,text="Audio Downloader",pady=20,font=title_fontstyle)
title.pack(side=TOP)

# URLs input
URL_frame=Frame(window)
URL_frame.pack(side=TOP,pady=20,padx=6)
URL_label=Label(URL_frame,text="Youtube URL: ",font=utility_fontstyle)
URL_entry=Entry(URL_frame,width=80,font=utility_fontstyle)
def render_queue(e=None):
    url= re.sub(" ","", URL_entry.get())
    if url != "":
        valid=downloader.append_URL(url)
        if valid:
            yt=YouTube(url)
            yt_objs=downloader.get_yt_objects()
            if [str(yt)for yt in yt_objs].count(str(yt))==1:
                board.render_url_inf(yt)
            else:
                board.render_warning_msg("[Duplicate url]: This url has been added before.")
        else:
            # messagebox.showerror("Invalid Youtube URL","[Invalid Youtube URL]   "+URL_entry.get())
            board.render_error_msg("[Unavailable url] "+URL_entry.get())
    URL_entry.delete(0,'end')
URL_btn=Button(URL_frame,text='+',font=utility_fontstyle,command=render_queue)

URL_label.pack(side=LEFT)
URL_entry.pack(side=LEFT)
URL_btn.pack(side=LEFT)

# board
board = Board(window)
board.pack()
window.bind('<Return>',render_queue)
downloader.set_board(board)

# config frame
def select_dir():
    path_=askdirectory()
    path.set(path_)

config_frame=Frame(window,pady=4)
config_frame.pack(side=TOP)

path_frame=Frame(config_frame)
path_frame.pack(side=TOP)
path_label=Label(path_frame,text="Destination: ",font=utility_fontstyle)
path_entry=Entry(path_frame,textvariable=path,state='readonly',width=60,font=utility_fontstyle)
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
    start_btn.config(state='disable',text="Converting...")
    start_btn.update()
    dir_path=str(path_entry.get())
    dBFS=int(normalize_entry.get().lstrip('-'))
    if normalize_entry.get()[0]=='-':
        dBFS=dBFS*(-1)
    if not os.path.isdir(dir_path):
        board.render_error_msg("Destination path: "+dir_path+" doesn't exists.")
        start_btn.config(state='active',text="Convert")
        start_btn.update()
        return False
    downloader.set_dir(path_entry.get())
    downloader.set_Format(format_combo.get())
    downloader.set_dBFS(dBFS)
    perfect=downloader.convert()
    
    if not perfect:
        board.render_error_msg("Something wents wrong! Check error messages above.")
    start_btn.config(state='active',text="Convert")
    start_btn.update()
    return perfect
start_frame=Frame(window,width=100,pady=40)
start_frame.pack()
start_btn=Button(start_frame,width=80,text='Convert',bg='white',command=start_convert,font=utility_fontstyle)
start_btn.pack(side=LEFT)

window.mainloop()