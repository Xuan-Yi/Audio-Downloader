from binascii import b2a_hex
import os
import shutil
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
        print(self.current_version)

    def download_7z(self):
        print('downloading 7zip...')
        self.zip_name = str(self.release_url).split(
            '/')[-1].replace("Audio.Downloader", "Audio Downloader")
        self.zip_path = os.path.join(os.getcwd(), self.zip_name)
        print("7zip path: ", self.zip_path)
        urllib.request.urlretrieve(self.release_url, self.zip_path)
        print("zip downloaded")

    def unzip_7z(self):
        print("unzipping...")
        self.folder_name = os.path.splitext(self.zip_name)[0]
        self.folder_dir = os.path.abspath("..")
        print("folder: ", self.folder_dir)
        with py7zr.SevenZipFile(self.zip_path, mode='r') as z:
            z.extractall(path=self.folder_dir)
        print("folder unzipped")

    def place_annihilator(self):
        # Place Annihilator.txt to new folder, then close program
        print("generating bat")
        self.annihilator_path = os.path.join(
            self.folder_dir, self.folder_name, "Annihilator.bat")
        print("bat: ", self.annihilator_path)
        with open(self.annihilator_path, 'x') as bat:
            bat.write(f'rd /s  "{os.path.abspath(os.getcwd())}" \n')
            print(os.path.abspath(os.getcwd()))
            print()
            bat.write('exit()')
        quit()
