import os
import shutil
from sys import exit
import string
import urllib
import py7zr


class update_handler:
    def __init__(self, release_url: string):
        # trigger
        if os.path.isfile("Annihilator.bat"):
            os.startfile("Annihilator.bat")
        # init
        self.release_url = release_url
        with open('version.txt', 'r') as f:
            self.current_version = f.read()

    def download_7z(self):
        self.zip_name = str(self.release_url).split(
            '/')[-1].replace("Audio.Downloader", "Audio Downloader")
        self.zip_path = os.path.join(os.getcwd(), self.zip_name)
        # delete existing 7zip
        if os.path.isfile(self.zip_path):
            os.remove(self.zip_path)
        # download 7zip
        urllib.request.urlretrieve(self.release_url, self.zip_path)

    def unzip_7z(self):
        self.folder_name = os.path.splitext(self.zip_name)[0]
        self.folder_dir = os.path.abspath("..")
        # delete existing diractory
        if os.path.isdir(os.path.join(self.folder_dir, self.folder_name)):
            shutil.rmtree(os.path.join(self.folder_dir, self.folder_name))
        # unzip
        with py7zr.SevenZipFile(self.zip_path, mode='r') as z:
            z.extractall(path=self.folder_dir)

    def place_annihilator(self):
        # Place Annihilator.txt to new folder, then close program
        self.annihilator_path = os.path.join(
            self.folder_dir, self.folder_name, "Annihilator.bat")
        # delete existing bat file
        if os.path.isfile(self.annihilator_path):
            os.remove(self.annihilator_path)
        with open(self.annihilator_path, 'x') as bat:
            bat.write(f'rd /s /q "{os.path.abspath(os.getcwd())}" \n')
            bat.write('exit()')
        exit()
