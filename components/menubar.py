import os
import shutil
import requests
import webbrowser
import py7zr
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from cores.auto_update import update_handler


def internet_connected():
    connection = os.system('ping www.google.com')
    if connection != 0:
        return False
    return True


class Menubar:
    def __init__(self, window: Tk):
        self.window = window
        self.fontStyle = tkFont.Font(family='Arial', size=12)  # font style
        self.check_version()  # read current and latest versions
        self.menubar = Menu(self.window, font=self.fontStyle, tearoff=False)
        try:
            self.update_handler = update_handler(self.release_url)
        except:
            self.update_handler = None
        # Information
        self.information_menu = Menu(self.menubar, tearoff=False)
        self.information_menu.add_command(
            label="Github repo", command=self.go_github_repo_callback)
        self.information_menu.add_command(
            label="Folder location", command=self.folder_location_callback)
        # function
        self.function_menu = Menu(self.menubar, tearoff=False)
        self.function_menu.add_command(
            label="Clear url queue", command=self.clear_url_queue_callback)
        # ffmpeg
        self.ffmpeg_menu = Menu(self.menubar, tearoff=False)
        self.ffmpeg_menu.add_command(
            label="Get ffmpeg.7z", command=self.get_ffmpeg_callback)
        self.ffmpeg_menu.add_command(
            label="Auto unzip ffmpeg.7z", command=self.unzip_ffmpeg_callback)
        # update menu
        self.update_menu = Menu(self.menubar, tearoff=False)
        self.update_menu.add_command(
            label="Current version", command=self.current_version_callback)
        self.update_menu.add_command(
            label="Check update", command=self.check_update_callback)

        self.menubar.add_cascade(
            label='Information', menu=self.information_menu)
        self.menubar.add_cascade(
            label='Function', menu=self.function_menu)
        self.menubar.add_cascade(label='ffmpeg', menu=self.ffmpeg_menu)
        self.menubar.add_cascade(label='Update', menu=self.update_menu)

        self.window.config(menu=self.menubar)

    def check_version(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases/latest")
            if response.status_code != 404:
                self.latest_version = response.json()['tag_name']
                self.release_url = str(response.json(
                )['assets'][0]['browser_download_url'])
            else:
                response = requests.get(
                    "https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases")
                self.latest_version = response.json()[0]['tag_name']
                self.release_url = response.json(
                )[0]['assets'][0]['browser_download_url']
            version_file = open('version.txt', 'r')
            self.current_version = version_file.read()
            version_file.close()
        except:
            if not internet_connected():
                return 'NO_INTERNET_CONNECTION'

    def is_latest_version(self):
        try:
            current_version = str(self.current_version).split(
                '.')  # convert string to array
            latest_version = str(self.latest_version).split(
                '.')  # convert string to array
            if int(latest_version[0].strip('v')) <= int(current_version[0].strip('v')):
                return True
            if int(latest_version[1]) <= int(current_version[1]):
                return True
            if int(latest_version[2]) <= int(current_version[2]):
                return True
            return False
        except:
            if not internet_connected():
                messagebox.showerror('No internet connection!',
                                     'Please check your internet connection.')

    def go_github_repo_callback(self):
        if internet_connected():
            webbrowser.open("https://github.com/Xuan-Yi/Audio-Downloader.git")
        else:
            messagebox.showerror('No internet connection!',
                                 'Please check your internet connection.')

    def folder_location_callback(self):
        messagebox.showinfo("Folder location", os.getcwd())

    def clear_url_queue_callback(self):
        queue_txt_path = os.path.abspath(
            os.path.join(os.getcwd(), 'queue.txt'))
        if os.path.isfile(queue_txt_path):
            os.remove(queue_txt_path)

    def get_ffmpeg_callback(self):
        if internet_connected():
            current_version = ""
            with open('version.txt', 'r') as f:
                current_version = f.read()
            webbrowser.open(
                "https://drive.google.com/file/d/13MSFs9cwRnn5hRCU5bDdMu-GsK39xB0P/view?usp=sharing")
            messagebox.showinfo("Download 7zip file",
                                f"Please download and place ffmpeg.7z under the folder Audio Downloader_{current_version}. Do not unzip it.")
        else:
            messagebox.showerror('No internet connection!',
                                 'Please check your internet connection.')

    def unzip_ffmpeg_callback(self):
        zip_path = os.path.join(os.getcwd(), 'ffmpeg.7z')
        ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg.exe')
        ffplay_path = os.path.join(os.getcwd(), 'ffplay.exe')
        ffprobe_path = os.path.join(os.getcwd(), 'ffprobe.exe')
        folder_path = os.path.join(os.getcwd(), 'ffmpeg')

        # remove existing files and folder
        file_list = [ffmpeg_path, ffplay_path, ffprobe_path]
        for f in file_list:
            if os.path.isfile(f):
                try:
                    os.remove(f)
                except OSError as e:
                    print(f"OSError: {e}")
        if os.path.isdir(folder_path):
            try:
                shutil.rmtree(folder_path)
            except OSError as e:
                print(f"OSError: {e}")
        # check if ffmpeg.7z exist
        is7zip = os.path.isfile(zip_path)
        if is7zip:
            perfect = True
            # unzip ffmpeg.7z
            try:
                with py7zr.SevenZipFile(zip_path, mode='r') as z:
                    z.extractall(path=os.path.abspath(os.getcwd()))
            except:
                perfect = False
                messagebox.showerror("Error", "Failed to unzip ffmpeg.7z.")
            # remove 7zip file
            try:
                os.remove(zip_path)
            except OSError as e:
                perfect = False
                messagebox.showerror("Error", "Failed to remove ffmpeg.7z.")
            if perfect:
                messagebox.showinfo("Success", "ffmpeg unziped successfully.")
        else:
            messagebox.showerror(
                "No file found", "Cannot find ffmpeg.7z.")

    def current_version_callback(self):
        if internet_connected():
            messagebox.showinfo('Current version',
                                f'Audio-Downloader_{self.current_version}')
        else:
            messagebox.showerror('No internet connection!',
                                 'Please check your internet connection.')

    def check_update_callback(self):
        if self.check_version() == 'NO_INTERNET_CONNECTION':
            messagebox.showerror('No internet connection!',
                                 'Please check your internet connection.')
            return False
        if self.is_latest_version():
            messagebox.showinfo(
                'Check update', f'Audio-Downloader_{self.current_version} is the latest version.')
        else:
            download = messagebox.askyesno(
                'Check update', f'New version released:\nAudio Downloader_{self.latest_version}\nWould you like to download it?')
            if download:
                # auto update
                try:
                    if self.update_handler == None:
                        self.check_version()
                        self.update_handler = update_handler(
                            self.release_url)
                    self.update_handler.download_7z()
                    self.update_handler.unzip_7z()
                    messagebox.showinfo(
                        "Success", f'Latest Audio Downloader is downloaded at {os.getcwd()}')
                except:
                    messagebox.showerror(
                        "Failed", 'Failed to auto download Audio Downloader, you can find release files at https://github.com/Xuan-Yi/Audio-Downloader/releases')
