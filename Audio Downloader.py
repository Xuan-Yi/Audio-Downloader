from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os

while True:
    links = input("The youtube URLs: ").split(" ")
    while True:
        audio_format = str(input("Audio format(mp3, wav, m4a, mp4):"))
        if audio_format not in ["mp3", "wav", "m4a", "mp4"]:
            print("Audio format should be one of below: mp3, wav, m4a, mp4.")
            continue
        break

    for link in links:
        yt = YouTube(link, on_progress_callback=on_progress)

        folder="./download audios"
        if not os.path.isdir(folder):
            os.makedirs(folder)

        yt.streams.get_audio_only().download(output_path = folder)

        if audio_format != 'mp4':
            new_name = folder+"/"+yt.title+" pytube."+audio_format
            if os.path.isfile(new_name):
                os.remove(new_name)
            ffmpeg.input(folder+"/"+yt.title+".mp4").output(new_name, f="wav").run()
            os.remove(folder+"/"+yt.title+".mp4")

