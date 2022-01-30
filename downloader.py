from tokenize import String
from turtle import title
from pytube import YouTube
from pytube.cli import on_progress
from pydub import AudioSegment
import os
import re

class AudioDownloader:
    def __init__(self,error_handler):
        self.error_handler=error_handler
        self.yt_objs=[]
        self.dir_path=os.getcwd()
        self.form="wav"
        self.dBFS=-6

    def set_Format(self,audio_form='m4a'):
        if audio_form in ["mp3", "wav", "m4a", "mp4"]:
            self.form=audio_form
        else:
            self.error_handler("Format not supported: ",audio_form)
            self.error_handler.to_txt()

    def set_dBFS(self,dBFS='-6'):
        self.dBFS=dBFS

    def set_dir(self,dir_path):
        self.dir_path=dir_path

    def get_yt_objects(self):
        return self.yt_objs
        
    def append_URL(self,url:String):
        # Check if URL is valid
        valid=False
        yt=None
        try:
            yt=YouTube(url)
            valid=yt.check_availability()==None
        except:
            valid=False

        if valid:
            self.yt_objs.append(yt)
        else:
            self.error_handler.addErr("Wrong URL: "+url)
            self.error_handler.to_txt()
        return valid

    def convert(self):
        perfect=True
        if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)

        for yt in self.yt_objs:       
            title=re.sub("\|||\/||\:||\*||\?||\'||\.||\"||\<||\>","",yt.title) # 處理特殊字元
            original_path = str(os.path.join(self.dir_path, title+".mp4"))
            '''if os.path.isfile(original_path):
                os.remove(original_path)'''

            try:
                yt.streams.get_audio_only().download(output_path=self.dir_path)
            except Exception as e:
                self.error_handler.addErr("Fail to download "+yt.title+": ")
                self.error_handler.addErr(str(e))
                self.error_handler.to_txt()
                perfect=False
                continue

            if self.form != 'mp4':
                try:
                    new_path = str(os.path.join(self.dir_path,title+"."+self.form))

                    if os.path.isfile(new_path):
                        os.remove(new_path)

                    def normalize(sound, target_dBFS):
                        change_in_dBFS = target_dBFS - sound.dBFS
                        return sound.apply_gain(change_in_dBFS)
                    
                    sound=AudioSegment.from_file(original_path,"m4a")
                    new_sound=normalize(sound,self.dBFS)
                    new_sound.export(new_path,self.form)
                    
                    os.remove(original_path)
                    print("["+title+"."+self.form+"]",
                        " has been downloaded successfully.")
                except Exception as e:
                    self.error_handler.addErr("ffmpeg error: "+str(e))
                    self.error_handler.to_txt()
                    perfect=False
                    continue
        if not perfect:
            return False
        return True