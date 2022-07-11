import string
from pytube import YouTube
from pytube.cli import on_progress
from pydub import AudioSegment
from components.board import Board
from tkinter import messagebox
import os

queue_txt_path = os.path.abspath(os.path.join(os.getcwd(), 'queue.txt'))
format_map = {'m4a': 'mp4', 'mp3': 'mp3', 'wav': 'wav', 'flac': 'flac'}


def internet_connected():
    connection = os.system('ping www.google.com')
    if connection != 0:
        return False
    return True


class AudioDownloader:
    def __init__(self):
        # self.yt_objs = []
        self.yt_queue = []  # {Youtube: (yt), url: (URL)}
        self.dir_path = os.getcwd()
        self.format = "wav"
        self.dBFS = -0.1
        self.initialized = False

    def init_yt_queue(self):
        try:
            if os.path.isfile(queue_txt_path):
                yt_urls = []
                with open(queue_txt_path, 'r') as f:
                    s = f.read()
                    yt_urls = s.split('$')
                    yt_urls = yt_urls[:-1]
                if yt_urls != []:
                    for i in range(len(yt_urls)):
                        yt_url = yt_urls[i]
                        yt_obj = YouTube(yt_url, on_progress_callback=self.board.on_progress,
                                         on_complete_callback=self.board.on_complete)
                        self.yt_queue.append({"yt": yt_obj, "url": yt_url})
                        self.board.render_url_inf(yt_obj)
            else:
                f = open(queue_txt_path, 'a+')
                f.close()
            self.initialized = True
        except:
            if not internet_connected():
                messagebox.showerror('No internet connection!',
                                     'Please check your internet connection.')
            self.initialized = False

    def set_Format(self, audio_format='m4a'):
        self.format = audio_format

    def set_dBFS(self, dBFS=0):
        self.dBFS = dBFS

    def set_dir(self, dir_path):
        if dir_path != "":
            self.dir_path = dir_path

    def set_board(self, board: Board):
        self.board = board

    def append_URL(self, url: string):
        # Check if URL is valid
        valid = False
        yt_obj = None
        try:
            yt_obj = YouTube(url, on_progress_callback=self.board.on_progress,
                             on_complete_callback=self.board.on_complete)
            valid = yt_obj.check_availability() == None
            if not self.initialized:
                self.init_yt_queue()

            if valid:
                if not str(yt_obj) in [str(yt) for yt in [self.yt_queue[z]['yt'] for z in range(len(self.yt_queue))]]:
                    with open(queue_txt_path, 'a') as queue_file:
                        queue_file.write(f'{url}$')
                    self.yt_queue.append({'yt': yt_obj, 'url': url})
                    self.board.render_url_inf(yt_obj)
                    return 'SUCCESS'
                else:
                    return 'DUPLICATE_URL'
        except:
            if not internet_connected():
                messagebox.showerror('No internet connection!',
                                     'Please check your internet connection.')
                return 'NO_INTERNET_CONNECTION'
        return 'URL_UNAVAILABLE'

    def normalize(self, sound, target_dBFS):
        if target_dBFS=='N':    # do not normalize
            return sound
        ratio = 0.99  # ratio of hard_normalization
        loudness_hard = sound.max_dBFS
        loudness_soft = sound.dBFS+3
        loudness = loudness_hard*ratio+loudness_soft*(1-ratio)
        change_in_dBFS = target_dBFS-loudness
        return sound.apply_gain(change_in_dBFS)

    def convert(self):
        if not internet_connected():
            return False
        else:
            if not self.initialized:
                self.init_yt_queue()
        perfect = True
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

        fail_list = []

        while len(self.yt_queue) != 0:
            yt_obj = self.yt_queue[0]
            yt = yt_obj['yt']
            url = yt_obj['url']
            self.board.render_download_inf("\nDownloading: "+yt.title)
            path_basic = os.path.join(self.dir_path, os.path.splitext(
                yt.streams.first().default_filename)[0])
            original_path = path_basic+".mp4"

            try:
                yt.streams.get_audio_only().download(output_path=self.dir_path)
                self.board.render_success_msg(
                    ""+yt.title+" is downloaded successfully.")
            except Exception as e:
                self.board.render_error_msg("Fail to download "+yt.title+": ")
                self.board.render_error_msg(str(e))
                perfect = False
                fail_list.append(url)
                self.yt_queue.remove(yt_obj)  # remove converted failed audio
                continue

            try:
                new_path = path_basic+"."+self.format

                if os.path.isfile(new_path):
                    os.remove(new_path)

                sound = AudioSegment.from_file(original_path)
                new_sound = self.normalize(sound, self.dBFS)
                new_sound.export(new_path, format_map[self.format])

                os.remove(original_path)
                self.board.render_success_msg(
                    ""+yt.title+" is convered successfully.\n")
            except Exception as e:
                self.board.render_error_msg("Convert error: "+str(e)+"\n")
                perfect = False
                fail_list.append(url)
                # remove converted failed audio
                self.yt_queue.remove(yt_obj)
                continue
            self.yt_queue.remove(yt_obj)  # remove converted audio
        os.remove('./queue.txt')
        with open('./queue.txt', 'a') as f:
            for l in fail_list:
                f.write(f'{l}$')
        if not perfect:
            return False
        else:
            return True
