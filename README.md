# Audio-Downloader

# Release
> [Audio Downloader_v1.1.0](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v1.1.0)
* This release works in my Win10, but not sure for other systems.
* Remember to **install ffmpeg**. See *Get ffmpeg* below.
* Please **DO NOT** move *Audio Downloader_v1.0.1.exe* out of the folder *Audio Downloader_v1.0.1*. You can place the folder anywhere.
* Instead, create a **shortcut(捷徑)**, then you can access *Audio Downloader_v1.0.1.exe* everywhere.

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
    > If you don't want to add these files to PATH,git  place them under the same layer where *Audio Downloader_vx.x.x* is.
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
    Pytube is powerful, but because of Youtube's fast technical change, issues occurs  frequently. (v_1.0.0 -> v_1.0.1, for example). It's recommended to  check [Issues of pytube](https://github.com/pytube/pytube/issues) when pytube breaks again. 
* [Pydub](https://github.com/jiaaro/pydub.git)
    ```
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