import string
from pytube import YouTube,Stream
from tkinter import *
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText


class Board:
    def __init__(self,window:Tk):
        self.window=window
        self.fontStyle=tkFont.Font(family='Arial',size=12)
        self.board=ScrolledText(window,wrap=WORD,width=90,height=12,bg='black',fg='white',font=self.fontStyle)
        self.board.config(state='disabled')
        # configs
        self.board.tag_config("url_config",foreground='white')
        self.board.tag_config("err_config",foreground='red')
        self.board.tag_config("warning_config",foreground='yellow')
        self.board.tag_config("progressbar_config",foreground='green')
        self.board.tag_config("any_config",foreground='white')
        
    def set_fontStyle(self,fontStyle:tkFont.Font):
        self.fontStyle=fontStyle

    def render_url_inf(self,yt:YouTube):
        if yt.check_availability()==None:
            self.board.config(state='normal')
            inf="[Add] "+yt.title+"\n"
            self.board.insert('insert',inf,'url_config')
            self.board.yview_pickplace('end')
            self.board.config(state='disabled')

    def render_error_msg(self,error:string):
        self.board.config(state='normal')
        self.board.insert('insert',error+"\n","err_config")
        self.board.yview_pickplace('end')
        self.board.config(state='disabled')

    def render_warning_msg(self,warning:string):
        self.board.config(state='normal')
        self.board.insert('insert',warning+"\n","warning_config")
        self.board.yview_pickplace('end')
        self.board.config(state='disabled')

    def render_any(self,message:string):
        self.board.config(state='normal')
        self.board.insert('insert',message+"\n","any_config")
        self.board.yview_pickplace('end')
        self.board.config(state='disabled')

    def on_progress(self,stream:Stream, chunk: bytes, bytes_remaining: int):
        filesize = stream.filesize
        bytes_received = filesize - bytes_remaining
        # progressbar
        ch: str = "█"
        max_width=36
        filled=int(round(max_width * bytes_received / float(filesize)))
        remaining=max_width-filled
        progress_bar = ch * filled + " " * remaining
        percent = round(100.0 * bytes_received / float(filesize), 1)
        text = f" ↳ |{progress_bar}| {percent}%\n"
        # write progressbar
        self.board.config(state='normal')
        self.board.insert('insert',text,"progressbar_config")
        self.board.yview_pickplace('end')
        self.board.config(state='disabled')

    def get_self(self):
        return self.board

    def clear(self):
        self.board.config(state='normal')
        self.board.delete('0.0',END)
        self.board.config(state='disabled')

    def pack(self):
        self.board.pack()