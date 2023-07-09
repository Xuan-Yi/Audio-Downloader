from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pytube import YouTube, extract
from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import urllib.request
import os
import numpy as np
import pandas as pd

formats = ['flac', 'mp3', 'm4a', 'wav']
format_map = {'m4a': 'mp4', 'mp3': 'mp3', 'wav': 'wav', 'flac': 'flac'}

shadowEffect = QGraphicsDropShadowEffect()
shadowEffect.setBlurRadius(4)
shadowEffect.setOffset(0, 0)
shadowEffect.setColor(QColor(0, 0, 0, 100))


class QueueUnit(QWidget):
    def __init__(self, funcs: list = [], youtube_url: str = "", props: dict = {}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.delete_unit_from_list] = funcs
        # youtube_url and props cannot be set at the same time
        if youtube_url != "" and props == {}:
            self.initData1(youtube_url)
        elif youtube_url == "" and props != {}:
            self.initData2(props)
        self.initQt()

    def initData1(self, _url: str):
        # youtube object
        self.youtube_obj = YouTube(_url)
        # id
        self.id = extract.video_id(_url)
        # thumbnail data
        url = self.youtube_obj.thumbnail_url   # derived from youtube_url
        self.__thumbnail_data = urllib.request.urlopen(url).read()
        # title text
        self.__title_text = self.youtube_obj.title
        self.__title_text = "".join(
            x for x in self.__title_text if x not in "\\/:*?\"<>|")
        # artist text
        self.__artist_text = self.youtube_obj.author
        self.__artist_text = "".join(
            x for x in self.__artist_text if x not in "\\/:*?\"<>|")

    def initData2(self, _props: dict):
        self.youtube_obj = _props['Youtube_obj']
        self.id = _props['ID']
        self.__thumbnail_data = _props['Thumbnail_data']
        self.__title_text = _props['Title']
        self.__artist_text = _props['Artist']

    def initQt(self):
        __validator = QRegExpValidator(
            QRegExp("^[^\\\\/:*?\"<>|]*$"))  # \\/:*?\"<>|
        self.state = 'WAITING'  # WAITING, WORKING, COMPLETE, FAILED

        '''# youtube object
        self.youtube_obj = YouTube(self.url)
        self.id = extract.video_id(self.url)'''
        self.url = "https://youtu.be/"+self.id  # simplest url

        # Components
        self.font = QFont('Segoe UI', 11)
        self.setFixedHeight(68)
        self.setAutoFillBackground(True)
        layout = QGridLayout()
        layout.setSpacing(18)

        # Thumbnail
        '''url = self.youtube_obj.thumbnail_url   # derived from youtube_url
        data = urllib.request.urlopen(url).read()'''
        image = QImage()
        image.loadFromData(self.__thumbnail_data)
        pixmap = QPixmap(image).scaled(64, 72, Qt.KeepAspectRatio)

        self.thumbnail = QLabel()
        self.thumbnail.setPixmap(pixmap)

        layout.addWidget(self.thumbnail, 0, 0, 1, 1)

        # Music title
        '''title = self.youtube_obj.title
        title = "".join(x for x in title if x not in "\\/:*?\"<>|")'''
        self.title = QLineEdit(text=f'{self.__title_text}', font=self.font)
        self.title.setValidator(__validator)
        self.title.setToolTip(self.title.text())
        self.title.setStyleSheet("QLineEdit {Background-color: transparent; padding: 2px; }"
                                 "QToolTip {background-color: white; color: black; border: 1px; }")
        self.title.setCursorPosition(0)
        layout.addWidget(self.title, 0, 1, 1, 10)

        # Artist
        '''artist = self.youtube_obj.author
        artist = "".join(x for x in artist if x not in "\\/:*?\"<>|")'''
        self.artist = QLineEdit(text=f'{self.__artist_text}', font=self.font)
        self.artist.setValidator(__validator)
        self.artist.setToolTip(self.artist.text())
        self.artist.setStyleSheet("QLineEdit {Background-color: transparent; padding: 2px; }"
                                  "QToolTip {background-color: white; color: black; border: 1px; }")
        self.artist.setCursorPosition(0)
        layout.addWidget(self.artist, 0, 11, 1, 4)

        # progress label
        self.progress_label = QLabel("", font=self.font)
        self.progress_label.setStyleSheet("QLabel {Background-color: transparent; padding: 2px; }"
                                          "QToolTip {background-color: white; color: black; border: 1px; }")
        layout.addWidget(self.progress_label, 0, 15, 1, 1)

        # Delete button
        self.delete_btn = QPushButton(text='✘', font=self.font)
        self.delete_btn.setStyleSheet('background-color: transparent;')
        self.delete_btn.setFixedSize(64, 32)
        self.delete_btn.clicked.connect(self.__delete_callback)
        layout.addWidget(self.delete_btn, 0, 16, 1, 1)

        self.setLayout(layout)

    def __delete_callback(self):
        self.delete_unit_from_list(self.id)

    def getID(self):
        return self.id

    def getYoutubeURL(self):
        return self.url

    def getYoutubeObj(self):
        return self.youtube_obj

    def getTitle(self):
        return self.title.text()

    def getArtist(self):
        return self.artist.text()

    def getState(self):
        return self.state

    def setEnabled(self, a0: bool):
        self.title.setReadOnly(not a0)
        self.title.setEnabled(a0)
        self.artist.setReadOnly(not a0)
        self.artist.setEnabled(a0)
        self.delete_btn.setEnabled(a0)

    def setInfos(self, title: str, artist: str):
        if title != "" and not pd.isnull(title):
            self.title.setText(title)
        if artist != "" and not pd.isnull(artist):
            self.artist.setText(artist)

    def createThread(self, dir: str, format: str):
        self.state = 'WORKING'
        self.progress_label.setText('📝')
        self.progress_label.setToolTip('Added to thread pool...')
        self.threadsignal = ThreadSignal()
        self.work = DownloadThread(self.threadsignal)
        self.work.setYoutubeObj(self.youtube_obj)
        self.work.setInfo(self.getTitle(), self.getArtist())
        self.work.setParams(dir, format)
        self.threadsignal.begin.connect(self.__on_begin)
        self.threadsignal.finish.connect(self.__on_complete)

    def getThread(self):
        return self.work

    def __on_begin(self):
        self.setEnabled(False)
        self.progress_label.setText('⏳')
        self.progress_label.setToolTip('Downloading...')

    def __on_complete(self, msg: str):
        self.errMsg = ""
        if msg == 'Success':
            self.progress_label.setText('✅')
            self.progress_label.setToolTip('Downloaded success.')
            self.setEnabled(True)
            self.state = 'COMPLETE'
        else:
            self.progress_label.setText('❌')
            self.progress_label.setToolTip(
                f'Downloaded failed.\n------\n{msg}')
            self.setEnabled(True)
            self.state = 'FAILED'
        '''if msg == 'Success':
            loop = QEventLoop()
            QTimer.singleShot(3000, loop.quit)
            loop.exec_()
            self.delete_unit_from_list(self.getID())'''


class ThreadSignal(QObject):
    begin = pyqtSignal()
    finish = pyqtSignal(str)  # 'Success' or error message

    def __init__(self):
        super().__init__()


class DownloadThread(QRunnable):
    def __init__(self, _ThreadSignal: ThreadSignal = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = _ThreadSignal

    def setYoutubeObj(self, yt: YouTube):
        self.youtube_obj = yt

    def setInfo(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def setParams(self, dir: str, format: str):
        self.dir = os.path.abspath(dir)
        self.format = format

    def run(self):
        self.signal.begin.emit()

        errMsg = ""  # error message

        default_name = os.path.join(self.dir, os.path.splitext(
            self.youtube_obj.streams.first().default_filename)[0])
        original_path = default_name+".mp4"
        if os.path.isfile(original_path):
            os.remove(original_path)

        try:
            self.youtube_obj.streams.get_audio_only().download(output_path=self.dir)
        except Exception as e:
            errMsg += f'pytube Error: {e}\n'
            pass

        # Convert audio file type
        try:
            file_name = os.path.join(self.dir, self.title)
            new_path = file_name+"."+self.format

            if os.path.isfile(new_path):
                os.remove(new_path)
            sound = AudioSegment.from_file(original_path)
            sound.export(new_path, format_map[self.format])
            os.remove(original_path)
        except Exception as e:
            errMsg += f'pydub Error: {e}'
            pass

        # Edit tags (do not support wav now)['flac','mp3','m4a','wav']
        if self.format == 'm4a':    # mp4
            # Edit mp4 tags (artist, thumbnail)
            audio = MP4(new_path)
            audio['\xa9ART'] = self.artist  # artist
            audio['aART'] = self.artist  # album artist
            url = self.youtube_obj.thumbnail_url   # derived from youtube_url
            data = urllib.request.urlopen(url).read()
            audio["covr"] = [MP4Cover(data, imageformat=MP4Cover.FORMAT_JPEG)]
            audio.save()
        elif self.format == 'flac':   # flac
            # Edit flac tags (artist, thumbnail)
            audio = FLAC(new_path)
            audio['ARTIST'] = self.artist  # artist
            audio['ALBUMARTIST'] = self.artist  # album artist
            url = self.youtube_obj.thumbnail_url   # derived from youtube_url
            data = urllib.request.urlopen(url).read()
            image = Picture()
            image.data = data
            audio.add_picture(image)
            audio.save()
        elif self.format == 'mp3':
            # Edit mp3 tags (artist, thumbnail)
            audio = EasyID3(new_path)
            audio['artist'] = self.artist  # artist
            audio['albumartist'] = self.artist  # album artist
            audio.save()
            audio = ID3(new_path)
            url = self.youtube_obj.thumbnail_url   # derived from youtube_url
            data = urllib.request.urlopen(url).read()
            audio['APIC'] = APIC(data=data)
            audio.save()

        if errMsg == "":
            self.signal.finish.emit('Success')
        else:
            print(f'Error: {errMsg}')
            self.signal.finish.emit(errMsg)
