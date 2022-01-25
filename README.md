# Audio-Downloader

# Introduction
* This tool is **NOT FOR COMMERCIAL USAGE**, please be careful when use this kind of programs.
* This tool would not be updated frequently.
* This tiny program use [pytube](https://github.com/pytube/pytube.git) to download audio. Then convert the audio format from mp4 to mp3, wav, m4a or mp4 with [ffmpeg](https://github.com/kkroening/ffmpeg-python.git).
* This tool has not had a GUI yet.

# Tutorial
* It's easy to use, since many functions of **pytube** and **ffmpeg** are sacrificed.
    ![](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)
1. **Paste the youtube URLs** of the audio you'd like to download. Mind, you can paste multiple URLs with each splited by a space, as showm above.
2. **Choose the audio format** you'd like to download as. Only
    * mp3
    * wav
    * m4a
    * mp4

    are available now, since they're most used in common life.
3. The audios would be stored in the folder **download audios**, wich is at the same layer of **Audio Downloader.exe**.
    ```
    |-  Audio Downloader.exe
    |-  download audios
        |-  <Your Audios>
    ```
