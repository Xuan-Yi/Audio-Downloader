import os
import requests
import webbrowser
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from cores.auto_update import update_handler


class Menubar:
    def __init__(self, window: Tk):
        self.window = window
        self.fontStyle = tkFont.Font(family='Arial', size=12)  # font style
        self.check_version()  # read current and latest versions
        self.menubar = Menu(self.window, font=self.fontStyle, tearoff=False)
        # Information
        self.information_menu = Menu(self.menubar, tearoff=False)
        self.information_menu.add_command(
            label="Github repo", command=self.go_github_repo_callback)
        self.information_menu.add_command(
            label="Folder location", command=self.folder_location_callback)
        # update menu
        self.update_menu = Menu(self.menubar, tearoff=False)
        self.update_menu.add_command(
            label="Current version", command=self.current_version_callback)
        self.update_menu.add_command(
            label="Check update", command=self.check_update_callback)

        self.menubar.add_cascade(
            label='Information', menu=self.information_menu)
        self.menubar.add_cascade(label='Update', menu=self.update_menu)

        self.window.config(menu=self.menubar)

    def check_version(self):
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

    def is_latest_version(self):
        current_version = str(self.current_version).split(
            '.')  # convert string to array
        latest_version = str(self.latest_version).split(
            '.')  # convert string to array
        if int(latest_version[0].strip('v')) > int(current_version[0].strip('v')):
            return False
        if int(latest_version[1]) > int(current_version[1]):
            return False
        if int(latest_version[2]) > int(current_version[2]):
            return False
        return True

    def go_github_repo_callback(self):
        webbrowser.open("https://github.com/Xuan-Yi/Audio-Downloader.git")

    def folder_location_callback(self):
        messagebox.showinfo("Folder location", os.getcwd())

    def current_version_callback(self):
        messagebox.showinfo('Current version',
                            f'Audio-Downloader_{self.current_version}')

    def check_update_callback(self):
        if self.is_latest_version():
            messagebox.showinfo(
                'Check update', f'Audio-Downloader_{self.current_version} is the latest version.')
        else:
            downlad = messagebox.askyesno(
                'Check update', f'New version released:\nAudio-Downloader_{self.latest_version}\nWould you like to auto update Audio Downloader?')
            if downlad:
                # auto update
                uh=update_handler(self.release_url)
                uh.download_7z()
                uh.unzip_7z()
                uh.place_mine()
                uh.trigger_mine()
                    
