# URL for test: https://youtu.be/9MpO8lw_Rj4
from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os

links = input("The youtube URLs: ").split(" ")
while True:
    audio_format = str(input("Audio format(mp3, wav, m4a, mp4):"))
    if audio_format not in ["mp3", "wav", "m4a", "mp4"]:
        print("Audio format should be one of below: mp3, wav, m4a, mp4.")
        continue
    break

for link in links:
    yt = YouTube(link, on_progress_callback=on_progress)

    folder = "./download audios"
    if not os.path.isdir(folder):
        os.makedirs(folder)

    original_path = folder+"/"+yt.title + ".mp4"
    if os.path.isfile(original_path):
        os.remove(original_path)

    try:
        yt.streams.get_audio_only().download(output_path=folder)
    except Exception as e:
        print("Error: ", e)

    if audio_format != 'mp4':
        try:
            new_path = folder+"/"+yt.title+"."+audio_format
            if os.path.isfile(new_path):
                os.remove(new_path)
            ffmpeg.input(folder+"/"+yt.title +
                         ".mp4").output(new_path, f="wav").run()
            os.remove(folder+"/"+yt.title+".mp4")
        except Exception as e:
            print("Error: ", e)
            print("original path: ", original_path)
            print("new path: ", new_path)
