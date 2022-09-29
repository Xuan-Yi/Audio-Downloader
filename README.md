# Audio-Downloader

# Release

Old version (please view instruction in earlier .md file.) :

> [Audio Downloader_v1.4.0](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v1.4.0)

New version:

> [Audio Downloader_v2.0.0](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v2.0.0)

- This release works in my Win10, but not sure for other systems.
- Please **DO NOT** move _Audio Downloader_vx.x.x.exe_ out of the folder _Audio Downloader_vx.x.x_. You can place the folder anywhere.
- Instead, create a **shortcut(捷徑)**, then you can access _Audio Downloader_vx.x.x.exe_ everywhere.

# Introduction

- This tool is **NOT FOR COMMERCIAL USAGE**, please be careful when use this kind of programs.
- This tiny program use [pytube](https://github.com/jiaaro/pydub.git) to download audio. Then convert the audio with [pydub](https://github.com/kkroening/ffmpeg-python.git) and add tags with [mutagen](https://pypi.org/project/mutagen/).
- Those are available auio formats:
  - flac
  - mp3
  - wav
  - m4a
- The GUI is powered by [PyQt5](https://pypi.org/project/PyQt5/)
- **pydub requires ffmpeg, install it by yourself.**

# Copyright

- [icon.ico](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)： <a href="https://www.flaticon.com/free-icons/headset" title="headset icons">Headset icons created by smalllikeart - Flaticon</a>

# Modules
* All modules are included in **./env.yaml**, you can simply create an environment by the command in Anaconda Prompt 
  ```
  conda env create -f <path of env.yaml>
  ```
  Again, remember to install ffmpeg on your computer.

- [PyQt5](https://pypi.org/project/PyQt5/)
  ```python
  # conda
  conda install -c anaconda pyqt
  ```

- [Pytube](https://github.com/pytube/pytube.git)
  ```python
  # pip
  pip install pytube
  ```
- [Pydub](https://github.com/jiaaro/pydub.git)
  ```python
  # pip
  pip install pydub
  ```
- [requests](https://github.com/psf/requests.git)
  ```python
  # pip
  pip install requests
  ```
- [pandas](https://pypi.org/project/pandas/)
  ```python
  # conda
  conda install pandas
  # pip
  pip install pandas
  ```
- [openpyxl](https://pypi.org/project/openpyxl/)
  ```python
  # conda
  conda install -c anaconda openpyxl
  # pip
  pip install openpyxl
  ```
- [mutagen](https://pypi.org/project/mutagen/)
  ```python
  # pip
  pip install mutagen
  ```


