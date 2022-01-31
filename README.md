# Audio-Downloader

# Release
* [Audio Downloader v1.0.0](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/1.0.0)

# Introduction
* This tool is **NOT FOR COMMERCIAL USAGE**, please be careful when use this kind of programs.
* This tiny program use [pytube](https://github.com/jiaaro/pydub.git) to download audio. Then produce the audio with [pydub](https://github.com/kkroening/ffmpeg-python.git).
* Those are available auio formats:
    * mp3
    * wav
    * m4a
    * mp4
* The GUI is powered by [tkinter](https://docs.python.org/3/library/tkinter.html)

# Get ffmpeg
Since [Pydub](https://github.com/jiaaro/pydub.git) depends on **ffmpeg**, **ffprobe**, and **ffplay**, you MUST install ffmpeg package. Please follow the tutorial below:
* Mac (use [homebrew](https://brew.sh/))
    ```
    brew install ffmpeg
    ```
* Linux (using aptitude):
    ```
    apt-get install ffmpeg
    ```
* Windows 
    1. Download and unzip folder [*youtbe-dl*](https://drive.google.com/file/d/1GLcJpqDi5DKNwHTfJU4EpfcLbmd6kK5K/view?usp=sharing), which includes 4 .exe files. 
        > Actually, *youtube-dl.exe* is not necessary, but you can access youtube-dl in your consoles if you don't delete *youtbe-dl.exe*.
    2. Add path of the folder *youtube-dl*, that is, `XX\youtube-dl` to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

# Copyright
* [icon.ico](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)： <a href="https://www.flaticon.com/free-icons/headset" title="headset icons">Headset icons created by smalllikeart - Flaticon</a>

# Modules
* [Pytube](https://github.com/pytube/pytube.git)
    ```
    pip install pytube
    ```
* [Pydub](https://github.com/jiaaro/pydub.git)
    ```
    pip install pydub
    ```

