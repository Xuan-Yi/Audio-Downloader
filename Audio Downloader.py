# URL for test: https://youtu.be/9MpO8lw_Rj4
import string
from tokenize import String
from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os
import time

folder = os.getcwd()+"/Audio Storage"


def Error_handler(msg: string = 'No message!', refresh: bool = False):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    err_path = folder+"/Err_Msg.txt"
    mode = "a+"
    if refresh:
        mode = "w+"
    file = open(err_path, mode)
    file.write(time.asctime(time.localtime(time.time()))+":  "+msg+'\r\n')
    file.close()


links = input("The youtube URLs: ").split(" ")
while True:
    audio_format = str(input("Audio format(mp3, wav, m4a, mp4):"))
    if audio_format not in ["mp3", "wav", "m4a", "mp4"]:
        print("Audio format should be one of below: mp3, wav, m4a, mp4.")
        continue
    break

for link in links:
    if not os.path.isdir(folder):
        os.makedirs(folder)

    try:
        yt = YouTube(link, on_progress_callback=on_progress)
    except Exception as e:
        Error_handler("Error: "+str(e))

    original_path = folder+"/"+yt.title+".mp4"
    if os.path.isfile(original_path):
        os.remove(original_path)

    try:
        yt.streams.get_audio_only().download(output_path=folder)
    except Exception as e:
        Error_handler("Error: "+str(e))

    if audio_format != 'mp4':
        try:
            new_path = folder+"/"+yt.title+"."+audio_format

            if os.path.isfile(new_path):
                os.remove(new_path)
            ffmpeg.input(original_path).output(new_path, f="wav").run()
            os.remove(original_path)
            print(yt.title+"."+audio_format,
                  " has been downloaded successfully.")
        except Exception as e:
            Error_handler("Error: "+str(e))
