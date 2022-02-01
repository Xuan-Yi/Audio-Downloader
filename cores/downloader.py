import string
from pytube import YouTube
from pytube.cli import on_progress
from pydub import AudioSegment
from components.board import Board
import os

class AudioDownloader:
    def __init__(self):
        self.yt_objs=[]
        self.dir_path=os.getcwd()
        self.format="wav"
        self.dBFS=-6

    def set_Format(self,audio_format='m4a'):
        if audio_format in ["mp3", "wav", "m4a", "mp4"]:
            self.format=audio_format
        else:
            self.board.render_error_msg("Format not supported: ",audio_format)

    def set_dBFS(self,dBFS='-6'):
        self.dBFS=dBFS

    def set_dir(self,dir_path):
        if dir_path!="":
            self.dir_path=dir_path

    def set_board(self,board:Board):
        self.board=board

    def get_yt_objects(self):
        return self.yt_objs
        
    def append_URL(self,url:string):
        # Check if URL is valid
        valid=False
        yt=None
        try:
            yt=YouTube(url,on_progress_callback=self.board.on_progress,on_complete_callback=self.board.on_complete)
            valid=yt.check_availability()==None
        except:
            valid=False

        if valid:
            if not str(yt) in [str(yt) for yt in self.yt_objs]:
                self.yt_objs.append(yt)
                return 'SUCCESS'
            else:
                return 'DUPLICATE_URL'
        return 'URL_UNAVAILABLE'

    def normalize(self,sound, target_dBFS):
        ratio=0.9 # ratio of hard_normalization
        loudness_hard=sound.max_dBFS
        loudness_soft=sound.dBFS+3
        loudness=loudness_hard*ratio+loudness_soft*(1-ratio)
        change_in_dBFS =  target_dBFS-loudness
        return sound.apply_gain(change_in_dBFS)

    def convert(self):
        perfect=True
        if not os.path.isdir(self.dir_path):
                os.mkdir(self.dir_path)

        queue_len=len(self.yt_objs)
        for i in range(queue_len):
            yt=self.yt_objs[0]
            self.board.render_download_inf("\nDownloading: "+yt.title)
            path_basic=os.path.join(self.dir_path,os.path.splitext(yt.streams.first().default_filename )[0])
            original_path=path_basic+".mp4"

            try:
                yt.streams.get_audio_only().download(output_path=self.dir_path)
                self.board.render_success_msg(""+yt.title+" is downloaded successfully.")
            except Exception as e:
                self.board.render_error_msg("Fail to download "+yt.title+": ")
                self.board.render_error_msg(str(e))
                perfect=False
                continue
            
            if self.format != 'mp4':
                try:
                    new_path=path_basic+"."+self.format

                    if os.path.isfile(new_path):
                        os.remove(new_path)
                    
                    sound=AudioSegment.from_file(original_path)
                    new_sound=self.normalize(sound,self.dBFS)
                    new_sound.export(new_path,self.format)
                    
                    os.remove(original_path)
                    self.yt_objs.remove(yt)
                    self.board.render_success_msg(""+yt.title+" is convered successfully.\n")
                except Exception as e:
                    self.board.render_error_msg("Convert error: "+str(e)+"\n")
                    perfect=False
                    continue
            else:
                self.board.render_success_msg(""+yt.title+" is convered successfully.\n")
            print("Left: "+str(len(self.yt_objs)))
            print("yt_objs: "+str([yt.author for yt in self.yt_objs]))
        if not perfect:
            return False
        else:
            return True