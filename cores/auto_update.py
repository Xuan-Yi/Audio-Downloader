import os
import shutil
import string
import urllib
import py7zr


class update_handler:
    def __init__(self, release_url: string):
        self.release_url = release_url
        with open('version.txt', 'r') as f:
            self.current_version = f.read()
        print(self.current_version)

    def download_7z(self):
        print('downloading 7zip...')
        self.zip_name = str(self.release_url).split('/')[-1].replace("Audio.Downloader","Audio Downloader")
        self.zip_path = os.path.join(os.getcwd(), self.zip_name)
        print("7zip path: ", self.zip_path)
        urllib.request.urlretrieve(self.release_url, self.zip_path)
        print("zip downloaded")

    def unzip_7z(self):
        print("unzipping...")
        self.folder_name = os.path.splitext(self.zip_name)[0]
        self.folder_path = os.path.join("..", self.folder_name)
        print("folder: ", self.folder_path)
        with py7zr.SevenZipFile(self.zip_path, mode='r') as z:
            z.extractall(path=self.folder_path)
        os.remove(self.zip_path)
        print("folder unzipped")

    def place_mine(self):
        # Place MINE.txt to new folder, then close program
        print("generating bat")
        exe_name = self.folder_name+".exe"
        self.mine_path = os.path.join(self.folder_path, "MINE.bat")  # .bat
        print("bat: ", self.mine_path)
        with open(self.mine_path, 'x') as bat:
            bat.write(f'@RD /S /Q "{os.getcwd()}"\n')
            bat.write(f'start /d "{self.folder_path}" "{exe_name}"')

    def trigger_mine(self):
        os.startfile(self.mine_path)
        quit()
