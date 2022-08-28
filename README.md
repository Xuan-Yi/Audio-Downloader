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

- [Pytube](https://github.com/pytube/pytube.git)
  ```
  pip install pytube
  ```
- [Pydub](https://github.com/jiaaro/pydub.git)
  ```python
  # To install from the source with pip
  python -m pip install git+https://github.com/pytube/pytube
  # To install from PyPI
  pip install pydub
  ```
- [requests](https://github.com/psf/requests.git)
  ```
  python -m pip install requests
  ```
