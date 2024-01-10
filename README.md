# Audio-Downloader

> I did this program for fun. Don't try to use it for illegal purposes.

* pydub requires [ffmpeg](https://ffmpeg.org/download.html), install it by yourself.
* Due to YouTube's policy, pytube may sometimes do not work properly.

```python
pip install PyQt5 pydub requests pandas openpyxl mutagen
python -m pip install git+https://github.com/pytube/pytube # install directly from repo for its frequent update
```

<!-- ## Release (Win11 only)

> [Audio Downloader_v2.0.2](https://github.com/Xuan-Yi/Audio-Downloader/releases/tag/v2.0.2)

* Please **DO NOT** move _Audio Downloader_vx.x.x.exe_ out of the folder _Audio Downloader_vx.x.x_. You can place the folder anywhere.
* Instead, create a **shortcut**, then you can access _Audio Downloader_vx.x.x.exe_ everywhere. -->

## Introduction

* **flac**, **mp3**, **wav**, and **m4a** are supproted.

### Basics

* Enqueue a song by the following steps.
* Please make sure that the directory is right.
![image](images/basics.jpg)

* It will generate an unit and push into the queue.
![image](images/queue.jpg)

### Import the music list (xlsx or csv)

* An example of format is shown below. Meaning of colums from left ot right are **title, artist, url** respectively.
* Content of first row isn't important, since this program will just skip it.

  ![image](images/xlsx_format.jpg)

* Import music list by **File > Import .xlsx**.

  ![image](images/import_xlsx.jpg)

## Copyright Claim

* [icon.ico](https://github.com/Xuan-Yi/Audio-Downloader/blob/main/readme_imgs/window.jpg)： [headset icons](https://www.flaticon.com/free-icons/headset) Headset icons created by smalllikeart - Flaticon
