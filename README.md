# Audio-Downloader

# Release
* [Audio Downloader v0.0.1](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v0.0.1)

# Introduction
* This tool is **NOT FOR COMMERCIAL USAGE**, please be careful when use this kind of programs.
* This tool may not be updated frequently.
* This tiny program use [pytube](https://github.com/pytube/pytube.git) to download audio. Then convert the audio format from mp4 to mp3, wav, m4a or mp4 with [ffmpeg](https://github.com/kkroening/ffmpeg-python.git).
* This tool has not had a GUI yet.

# Modules
* [Pytube](https://github.com/pytube/pytube.git): `pip install pytube`
* [Pydub](https://github.com/jiaaro/pydub.git): `pip install pydub`

# Tutorial
## [Audio Downloader.exe]((https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v0.0.1))
* It's easy to use, since many functions of **pytube** and **ffmpeg** are sacrificed.
    ![](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)
1. **Paste the youtube URLs** of the audio you'd like to download. Mind, you can paste multiple URLs with each splited by a space, as showm above.
2. **Choose the audio format** you'd like to download as. Only
    * mp3
    * wav
    * m4a
    * mp4

    are available now, since they're most used in common life.
3. The audios would be stored in the folder **Audio Storage**, wich is at the same layer of **Audio Downloader.exe**. If some error occur, the error message will be written in **Err_Msg.txt**.
    ```
    Audio Downloader
        |-  Audio Downloader.exe
        |-  Audio Storage
            |-  (Err_Msg.txt)
            |-  <Your Audios>
    ```
## Get ffmpeg
* Mac (use [homebrew](https://brew.sh/))
    ```
    brew install ffmpeg
    ```
* Linux (using aptitude):
    ```
    apt-get install ffmpeg libavcodec-extra
    ```
* Windows 
    1. Download and unzip [*youtbe-dl*](https://drive.google.com/file/d/1GLcJpqDi5DKNwHTfJU4EpfcLbmd6kK5K/view?usp=sharing), which is a folder including **ffmpeg.exe** and **youtube-dl.exe**. Actually, *youtube-dl.exe* is not necessary, but you can access youtube-dl in your consoles if you don't delete *youtbe-dl.exe*.
    2. Then add path of folder *youtube-dl*, that is, `XX\youtube-dl` to PATH.

# Copyright
* [icon.ico](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)： <a href="https://www.flaticon.com/free-icons/headset" title="headset icons">Headset icons created by smalllikeart - Flaticon</a>

