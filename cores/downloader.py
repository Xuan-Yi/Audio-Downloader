import string
from pytube import YouTube
from pytube.cli import on_progress
from pydub import AudioSegment
from components.board import Board
import os


class AudioDownloader:
    def __init__(self):
        self.yt_objs = []
        self.dir_path = os.getcwd()
        self.format = "wav"
        self.dBFS = -6
        
    def set_Format(self, audio_format='m4a'):
        if audio_format in ["mp3", "wav", "m4a", "mp4"]:
            self.format = audio_format
        else:
            self.board.render_error_msg("Format not supported: ", audio_format)

    def set_dBFS(self, dBFS=0):
        print('dBFS: ',dBFS)
        self.dBFS = dBFS

    def set_dir(self, dir_path):
        if dir_path != "":
            self.dir_path = dir_path

    def set_board(self, board: Board):
        self.board = board

    def get_yt_objects(self):
        return self.yt_objs

    def refresh_yt_objs(self):
        queue_txt_path=os.path.abspath(os.path.join(os.getcwd(),'queue.txt'))
        if os.path.isfile(queue_txt_path):
            yt_urls = []
            with open('./queue.txt', 'r') as f:
                s = f.read()
                yt_urls = s.split('$')
            yt_urls=yt_urls[:-1]
            print('yt_urls: ',yt_urls)
            if yt_urls != []:
                self.yt_objs = []
                for i in range(len(yt_urls)):
                    self.yt_objs.append(YouTube(
                        yt_urls[i], on_progress_callback=self.board.on_progress, on_complete_callback=self.board.on_complete))

    def append_URL(self, url: string):
        self.refresh_yt_objs()
        # Check if URL is valid
        valid = False
        yt = None
        try:
            yt = YouTube(url, on_progress_callback=self.board.on_progress,
                         on_complete_callback=self.board.on_complete)
            valid = yt.check_availability() == None
        except:
            valid = False

        if valid:
            if not str(yt) in [str(yt) for yt in self.yt_objs]:
                queue_txt_path=os.path.abspath(os.path.join(os.getcwd(),'queue.txt'))
                with open(queue_txt_path, 'a') as queue_file:
                    queue_file.write(f'{url}$')  # recognize \n\t\n\t
                return 'SUCCESS'
            else:
                return 'DUPLICATE_URL'
        return 'URL_UNAVAILABLE'

    def normalize(self, sound, target_dBFS):
        ratio = 1.0  # ratio of hard_normalization
        loudness_hard = sound.max_dBFS
        loudness_soft = sound.dBFS+3
        loudness = loudness_hard*ratio+loudness_soft*(1-ratio)
        change_in_dBFS = target_dBFS-loudness
        return sound.apply_gain(change_in_dBFS)

    def convert(self):
        self.refresh_yt_objs()
        perfect = True
        if not os.path.isdir(self.dir_path):
            os.mkdir(self.dir_path)

        fail_list=[]
        queue_list=[]
        with open('./queue.txt','r') as f:
            s=f.read()
            queue_list=s.split('$')
            queue_list=queue_list[:-1]
        print('queue_list: ',queue_list)
        print('yt_objs: ',type(self.yt_objs[0]))

        for i in range(len(self.yt_objs)):
            yt = self.yt_objs[0]
            print("yt: ",yt)
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
                fail_list.append(queue_list[i])
                continue

            if self.format != 'mp4':
                try:
                    new_path = path_basic+"."+self.format

                    if os.path.isfile(new_path):
                        os.remove(new_path)

                    sound = AudioSegment.from_file(original_path)
                    new_sound = self.normalize(sound, self.dBFS)
                    new_sound.export(new_path, self.format)

                    os.remove(original_path)
                    self.yt_objs.remove(yt)
                    self.board.render_success_msg(
                        ""+yt.title+" is convered successfully.\n")
                except Exception as e:
                    self.board.render_error_msg("Convert error: "+str(e)+"\n")
                    perfect = False
                    continue
            else:
                self.board.render_success_msg(
                    ""+yt.title+" is convered successfully.\n")
        os.remove('./queue.txt')
        with open('./queue.txt','a') as f:
            for l in fail_list:
                f.write(f'{l}$')
        if not perfect:
            return False
        else:
            return True
