# Audio-Downloader

# Release
> [Audio Downloader_v1.4.0](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v1.4.0)
* This release works in my Win10, but not sure for other systems.
* Remember to **install ffmpeg**. See *Get ffmpeg* below.
* Please **DO NOT** move *Audio Downloader_vx.x.x.exe* out of the folder *Audio Downloader_vx.x.x*. You can place the folder anywhere.
* Instead, create a **shortcut(捷徑)**, then you can access *Audio Downloader_vx.x.x.exe* everywhere.

# Introduction
* This tool is **NOT FOR COMMERCIAL USAGE**, please be careful when use this kind of programs.
* This tiny program use [pytube](https://github.com/jiaaro/pydub.git) to download audio. Then produce the audio with [pydub](https://github.com/kkroening/ffmpeg-python.git).
* Those are available auio formats:
    * mp3
    * wav
    * mp4
* The GUI is powered by [tkinter](https://docs.python.org/3/library/tkinter.html)

# Get ffmpeg
## Method 1 (more convenient than method 2)
In the menu of Audio Downloader_vx.x.x, select *ffmpeg*, then you will get the 7zip file (download it but DO NOT unzip it). Just follow the instructions.
## Method 2 (method 1 is easier)
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
    > If you don't want to add these files to PATH,  place them under the same layer where *Audio Downloader_vx.x.x* is.
    1. Download and unzip folder [*ffmpeg.7z*](https://drive.google.com/file/d/13MSFs9cwRnn5hRCU5bDdMu-GsK39xB0P/view?usp=sharing), which includes 3 .exe files. 
    2. Add path of the folder *ffmpeg*, that is, `XX\ffmpeg` to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

# Copyright
* [icon.ico](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)： <a href="https://www.flaticon.com/free-icons/headset" title="headset icons">Headset icons created by smalllikeart - Flaticon</a>

# Modules
* [Pytube](https://github.com/pytube/pytube.git)
    ```
    pip install pytube
    ```
* [Pydub](https://github.com/jiaaro/pydub.git)
    ```python
    # To install from the source with pip
    python -m pip install git+https://github.com/pytube/pytube
    # To install from PyPI
    pip install pydub
    ```
* [requests](https://github.com/psf/requests.git)
    ```
    python -m pip install requests
    ```
* [py7zr](https://github.com/miurahr/py7zr.git)
    ```
    pip install py7zr
    ```