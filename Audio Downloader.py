from multiprocessing import connection, queues
import os
import re
import string
from sys import exit
import tkinter
from tokenize import String
from pytube import YouTube
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askdirectory
import tkinter.ttk as ttk
from cores.downloader import AudioDownloader
from components.board import Board
from components.menubar import Menubar

# Check connection
connection = os.system('ping www.google.com')

if connection != 0:
    window = Tk()
    window.resizable(False, False)
    window.withdraw()
    messagebox.showerror("No internet connection",
                         "Cannot open Audio Downloader.\nPleace check your connection.")
else:
    folder = os.getcwd()
    downloader = AudioDownloader()

    # GUI
    window = Tk()
    window.resizable(False, False)
    window.title('Audio Downloader')
    window.iconbitmap("./images/icon.ico")

    title_fontstyle = tkFont.Font(family='Arial', size=16)
    utility_fontstyle = tkFont.Font(family='Arial', size=12)
    queue_fontstyle = tkFont.Font(family='Ubuntu Light', size=12)

    path = StringVar(value=os.getcwd())
    URLs = StringVar()

    title = Label(window, text="Audio Downloader",
                  pady=20, font=title_fontstyle)
    title.pack(side=TOP)

    # Menubar
    Menubar = Menubar(window)

    # URLs input
    URL_frame = Frame(window)
    URL_frame.pack(side=TOP, pady=20, padx=6)
    URL_label = Label(URL_frame, text="Youtube URL: ", font=utility_fontstyle)
    URL_entry = Entry(URL_frame, width=80, font=utility_fontstyle)

    def render_queue(e=None):
        url = re.sub(" ", "", URL_entry.get())
        if url != "":
            return_msg = downloader.append_URL(url)
            if return_msg == 'SUCCESS':
                yt = YouTube(url)
                board.render_url_inf(yt)
            elif return_msg == 'DUPLICATE_URL':
                messagebox.showwarning(
                    'Duplicate url', 'This url has been added.')
            elif return_msg == 'URL_UNAVAILABLE':
                messagebox.showerror(
                    'Unavailable url', f'{URL_entry.get()} \nis not a valid Youtube url or is unavailable.')
        URL_entry.delete(0, 'end')

    URL_btn = Button(URL_frame, text='+', state='active',
                     font=utility_fontstyle, command=render_queue)

    URL_label.pack(side=LEFT)
    URL_entry.pack(side=LEFT)
    URL_btn.pack(side=LEFT)

    # board
    board = Board(window)
    board.pack()
    window.bind('<Return>', render_queue)
    downloader.set_board(board)

    # config frame

    def select_dir():
        path_ = askdirectory()
        print('path: ', path_, '\ttype: ', type(path_))
        if path_ != '':
            path.set(path_)

    config_frame = Frame(window, pady=4)
    config_frame.pack(side=TOP)

    path_frame = Frame(config_frame)
    path_frame.pack(side=TOP)
    path_label = Label(path_frame, text="Destination: ",
                       font=utility_fontstyle)
    path_entry = Entry(path_frame, textvariable=path,
                       state='readonly', width=60, font=utility_fontstyle)
    path_btn = Button(path_frame, command=select_dir,
                      text="Search", font=utility_fontstyle)
    path_entry.insert(0, os.getcwd())
    path_label.pack(side=LEFT)
    path_entry.pack(side=LEFT)
    path_btn.pack(side=LEFT)

    format_frame = Frame(config_frame)
    format_frame.pack(side=LEFT)
    format_label = Label(format_frame, text="Audio format: ",
                         font=utility_fontstyle)
    format_combo = ttk.Combobox(format_frame, value=[
                                "wav", "mp3", "mp4"], state='readonly', width=6, font=utility_fontstyle)
    format_combo.current(0)
    format_label.pack(side=LEFT)
    format_combo.pack(side=LEFT)

    normalize_frame = Frame(config_frame)
    normalize_frame.pack(side=RIGHT)

    def normalize_validate(dBFS: str):
        for c in dBFS:
            if c not in ['-', '.', ' ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                normalize_entry.delete(0, 'end')
                normalize_entry.insert(0, '-0.1')
                messagebox.showwarning(
                    'Invalid dBFS', 'dBFS should be a number ≤0')
                return False
        if dBFS == '0':
            return True
        # quit invalid raw dBFS
        if len(re.findall('\.', dBFS)) > 1 or len(re.findall('-', dBFS)) > 1 or dBFS[0] != '-':
            normalize_entry.delete(0, 'end')
            normalize_entry.insert(0, '-0.1')
            messagebox.showwarning(
                'Invalid dBFS', 'dBFS should be a number ≤0')
            return False
        # define raw dBFS to acceptable format
        if ' ' in dBFS:
            dBFS = dBFS.split()
            dBFS.join()
        while dBFS[1] == '0' and dBFS[2] != '.':
            dBFS = '-'+dBFS[2:]
        if dBFS[1] == '.':
            dBFS = '-0'+dBFS[1:]
        if len(re.findall('\.', dBFS)) == 0:
            dBFS = dBFS+'.0'
        normalize_entry.delete(0, 'end')
        normalize_entry.insert(0, dBFS)
        return True

    valid_cmd = (config_frame.register(normalize_validate), "%P")
    normalize_label1 = Label(
        normalize_frame, text="Normalize to ", font=utility_fontstyle)
    normalize_entry = Entry(normalize_frame, validate='focusout',
                            width=6, validatecommand=valid_cmd, font=utility_fontstyle,)
    normalize_label2 = Label(
        normalize_frame, text=" dBFS", font=utility_fontstyle)
    normalize_entry.insert(0, '-0.1')
    normalize_label1.pack(side=LEFT)
    normalize_entry.pack(side=LEFT)
    normalize_label2.pack(side=LEFT)

    # START button
    def convert_dBFS_to_double(dBFS_str: str):
        if dBFS_str == '0':
            return 0
        dBFS_ = dBFS_str.split(sep='.')
        print('dBFS array: ', int(dBFS_[0]), int(dBFS_[1]))
        dBFS = int(dBFS_[0])-int(dBFS_[1])*pow(10, ((-1)*len(dBFS_[1])))
        return dBFS

    def start_convert():
        dir_path = str(path_entry.get())
        # check dBFS is in acceptable form
        if normalize_validate(normalize_entry.get()) == False:
            return False
        dBFS = convert_dBFS_to_double(normalize_entry.get())
        # check the target directory exists
        if not os.path.isdir(dir_path):
            board.render_error_msg("[Invalid destination path]: "+dir_path)
            window.update()
            return False

        URL_entry.config(state='readonly')
        URL_btn.config(state='disabled', text='X')
        format_combo.config(state='readonly')
        normalize_entry.config(state='readonly')
        path_entry.config(state='readonly')
        path_btn.config(state='disable')
        start_btn.config(state='disabled', text="Converting...")
        window.update()
        downloader.set_dir(path_entry.get())
        downloader.set_Format(format_combo.get())
        downloader.set_dBFS(dBFS)

        perfect = downloader.convert()
        if not perfect:
            board.render_error_msg(
                "Something wents wrong! Check error messages above.")
        URL_entry.config(state='normal')
        URL_btn.config(state='active', text='+')
        format_combo.config(state='normal')
        normalize_entry.config(state='readonly')
        path_entry.config(state='normal')
        path_btn.config(state='normal')
        start_btn.config(state='active', text="Convert")
        window.update()
        return perfect

    start_frame = Frame(window, width=100, pady=40)
    start_frame.pack()
    start_btn = Button(start_frame, width=80, state='active', text='Convert',
                       bg='white', command=start_convert, font=utility_fontstyle)
    start_btn.pack(side=LEFT)

    window.mainloop()
