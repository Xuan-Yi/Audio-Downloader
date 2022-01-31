import string
from pytube import YouTube
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
            yt=YouTube(url,on_progress_callback=self.board.on_progress)
            valid=yt.check_availability()==None
        except:
            valid=False

        if valid:
            if yt not in self.yt_objs:
                self.yt_objs.append(yt)
        return valid

    def convert(self):
        perfect=True
        if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)

        for yt in self.yt_objs:
            self.board.render_any("\nDownloading: "+yt.title+"")
            path_basic=os.path.join(self.dir_path,os.path.splitext(yt.streams.first().default_filename )[0])
            original_path=path_basic+".mp4"

            try:
                yt.streams.get_audio_only().download(output_path=self.dir_path)
                self.board.render_any(""+yt.title+" is downloaded successfully.\n")
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

                    def normalize(sound, target_dBFS):
                        ratio=0.2 # ratio of limiter
                        loudness_hard=sound.max_dBFS
                        loudness_soft=sound.dBFS+3
                        loudness=loudness_soft*ratio+loudness_hard*(1-ratio)
                        change_in_dBFS =  target_dBFS-loudness
                        return sound.apply_gain(change_in_dBFS)
                    
                    sound=AudioSegment.from_file(original_path,"m4a")
                    new_sound=normalize(sound,self.dBFS)
                    new_sound.export(new_path,self.format)
                    
                    os.remove(original_path)
                    self.yt_objs.remove(yt)
                except Exception as e:
                    self.board.render_error_msg("Convert error: "+str(e))
                    perfect=False
                    continue
        if not perfect:
            return False
        return True