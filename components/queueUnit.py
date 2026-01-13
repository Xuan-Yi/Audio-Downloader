from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from pytubefix import YouTube, extract
from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

import urllib.request
import os
import numpy as np
import pandas as pd

formats = ["flac", "mp3", "m4a", "wav"]
format_map = {"m4a": "mp4", "mp3": "mp3", "wav": "wav", "flac": "flac"}


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
        url = self.youtube_obj.thumbnail_url  # derived from youtube_url
        self.__thumbnail_data = urllib.request.urlopen(url).read()
        # title text
        self.__title_text = self.youtube_obj.title
        self.__title_text = "".join(x for x in self.__title_text if x not in '\\/:*?"<>|')
        # artist text
        self.__artist_text = self.youtube_obj.author
        self.__artist_text = "".join(x for x in self.__artist_text if x not in '\\/:*?"<>|')

    def initData2(self, _props: dict):
        self.youtube_obj = _props["Youtube_obj"]
        self.id = _props["ID"]
        self.__thumbnail_data = _props["Thumbnail_data"]
        self.__title_text = _props["Title"]
        self.__artist_text = _props["Artist"]

    def initQt(self):
        __validator = QRegularExpressionValidator(QRegularExpression('^[^\\\\/:*?"<>|]*$'))  # \\/:*?\"<>|
        self.state = "WAITING"  # WAITING, WORKING, COMPLETE, FAILED
        self.url = "https://youtu.be/" + self.id

        # Main Layout for the Widget
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)

        # Card Frame
        self.card = QFrame()
        self.card.setObjectName("Card")
        self.card.setStyleSheet(Theme.card_style())

        # Inner Layout (Horizontal)
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Thumbnail
        image = QImage()
        image.loadFromData(self.__thumbnail_data)
        pixmap = QPixmap(image).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        # Crop to square or rounded rect if needed, for now just nice scaling

        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(80, 60)
        self.thumbnail.setPixmap(pixmap)
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setStyleSheet(f"border-radius: 4px; border: 1px solid {Theme.BORDER};")

        layout.addWidget(self.thumbnail)

        # Info Layout (Vertical: Title, Artist)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        info_layout.setContentsMargins(0, 0, 0, 0)

        # Music title
        self.title = QLineEdit(text=f"{self.__title_text}")
        self.title.setPlaceholderText("Title")
        self.title.setValidator(__validator)
        self.title.setToolTip(self.title.text())
        self.title.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_PRIMARY}; font-weight: bold; font-size: 11pt;")
        self.title.setCursorPosition(0)

        # Artist
        self.artist = QLineEdit(text=f"{self.__artist_text}")
        self.artist.setPlaceholderText("Artist")
        self.artist.setValidator(__validator)
        self.artist.setToolTip(self.artist.text())
        self.artist.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_SECONDARY}; font-size: 10pt;")
        self.artist.setCursorPosition(0)

        info_layout.addWidget(self.title)
        info_layout.addWidget(self.artist)

        layout.addLayout(info_layout, 1)

        # Status & Action Layout
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)

        # progress label

        self.progress_label = QLabel("")

        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.updateStatusDisplay()

        action_layout.addWidget(self.progress_label)

        

        # Delete button
        self.delete_btn = QPushButton("X")
        self.delete_btn.setFixedSize(32, 32)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setToolTip("Remove from queue")
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ERROR};
                color: white;
                border: 1px solid {Theme.ERROR};
            }}
        """)
        self.delete_btn.clicked.connect(self.__delete_callback)
        action_layout.addWidget(self.delete_btn)

        layout.addLayout(action_layout)

        self.card.setLayout(layout)
        main_layout.addWidget(self.card)

        self.setLayout(main_layout)
        self.setFixedHeight(100)  # Slightly taller to accommodate padding
        self.setMinimumWidth(380) # Ensure content fits horizontally

    def __delete_callback(self):
        self.delete_unit_from_list(self.id)

    def updateStatusDisplay(self):
        base_style = """
            QLabel {
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: bold;
            }
        """

        if self.state == "WAITING":
            text = "Pending"
            bg = Theme.SECONDARY_PRESSED
            color = Theme.TEXT_SECONDARY
            border = f"1px solid {Theme.BORDER}"
            tooltip = "Waiting in queue..."
        elif self.state == "WORKING":
            text = "Downloading"
            bg = Theme.PRIMARY
            color = "#ffffff"
            border = "none"
            tooltip = "Downloading..."
        elif self.state == "COMPLETE":
            text = "Finished"
            bg = Theme.SUCCESS
            color = "#ffffff"
            border = "none"
            tooltip = "Download success"
        elif self.state == "FAILED":
            text = "Failed"
            bg = Theme.ERROR
            color = "#ffffff"
            border = "none"
            tooltip = f"Download failed"
        else:
            text = self.state
            bg = Theme.SECONDARY
            color = Theme.TEXT_PRIMARY
            border = "none"
            tooltip = ""

        self.progress_label.setText(text)

        self.progress_label.setToolTip(tooltip)

        self.progress_label.setFixedSize(85, 20)

        self.progress_label.setStyleSheet(base_style + f"""

            QLabel {{

                background-color: {bg};

                color: {color};

                border: {border};

            }}

        """)

        

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
        self.state = "WORKING"
        self.updateStatusDisplay()
        self.threadsignal = ThreadSignal()
        self.work = DownloadThread(self.threadsignal)
        self.work.setUrl(self.url)
        self.work.setInfo(self.getTitle(), self.getArtist())
        self.work.setParams(dir, format)
        self.threadsignal.begin.connect(self.__on_begin)
        self.threadsignal.finish.connect(self.__on_complete)

    def getThread(self):
        return self.work

    def __on_begin(self):
        self.setEnabled(False)
        # self.state is already set to WORKING in createThread, but ensure display is updated
        self.updateStatusDisplay()

    def __on_complete(self, msg: str):
        self.errMsg = ""
        if msg == "Success":
            self.state = "COMPLETE"
            self.updateStatusDisplay()
            self.setEnabled(True)
        else:
            self.state = "FAILED"
            self.updateStatusDisplay()
            self.progress_label.setToolTip(f"Downloaded failed.\n------\n{msg}")
            self.setEnabled(True)

    def updateTheme(self):
        self.card.setStyleSheet(Theme.card_style())
        self.thumbnail.setStyleSheet(f"border-radius: 4px; border: 1px solid {Theme.BORDER};")
        self.title.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_PRIMARY}; font-weight: bold; font-size: 11pt;")
        self.artist.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_SECONDARY}; font-size: 10pt;")
        self.updateStatusDisplay()
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: {Theme.ERROR};
                color: white;
                border: 1px solid {Theme.ERROR};
            }}
        """)


class ThreadSignal(QObject):
    begin = pyqtSignal()
    finish = pyqtSignal(str)  # 'Success' or error message

    def __init__(self):
        super().__init__()


class DownloadThread(QRunnable):
    def __init__(self, _ThreadSignal: ThreadSignal = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = _ThreadSignal
        self.url = ""

    def setUrl(self, url: str):
        self.url = url

    def setInfo(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def setParams(self, dir: str, format: str):
        self.dir = os.path.abspath(dir)
        self.format = format

    def run(self):
        self.signal.begin.emit()

        errMsg = ""  # error message
        original_path = ""

        # Create a fresh YouTube object to avoid stale URLs
        try:
            yt = YouTube(self.url)
        except Exception as e:
            errMsg += f"Connection Error: {e}\n"
            self.signal.finish.emit(errMsg)
            return

        try:
            # download returns the file path
            stream = yt.streams.get_audio_only()
            if stream is None:
                # Fallback: try filtering manually
                stream = yt.streams.filter(only_audio=True).first()

            if stream:
                original_path = stream.download(output_path=self.dir)
            else:
                errMsg += "Error: No audio stream found for this video.\n"

        except Exception as e:
            errMsg += f"pytubefix Error: {e}\n"

        new_path = ""
        # Convert audio file type
        if errMsg == "":
            try:
                file_name = os.path.join(self.dir, self.title)
                new_path = file_name + "." + self.format

                # Normalize paths for comparison
                abs_new = os.path.abspath(new_path)
                abs_orig = os.path.abspath(original_path)

                if abs_new != abs_orig:
                    if os.path.isfile(new_path):
                        os.remove(new_path)

                    # Check if original_path exists before converting
                    if os.path.exists(original_path):
                        sound = AudioSegment.from_file(original_path)
                        sound.export(new_path, format_map[self.format])
                        os.remove(original_path)
                    else:
                        errMsg += f"Download failed: File not found at {original_path}"

                # If paths are the same, the file is already where it needs to be.

            except Exception as e:
                errMsg += f"pydub Error: {e}"

        # Edit tags (do not support wav now)['flac','mp3','m4a','wav']
        if errMsg == "" and os.path.exists(new_path):
            try:
                if self.format == "m4a":  # mp4
                    # Edit mp4 tags (artist, thumbnail)
                    audio = MP4(new_path)
                    audio["\xa9ART"] = self.artist  # artist
                    audio["aART"] = self.artist  # album artist
                    url = yt.thumbnail_url  # derived from youtube_url
                    data = urllib.request.urlopen(url).read()
                    audio["covr"] = [MP4Cover(data, imageformat=MP4Cover.FORMAT_JPEG)]
                    audio.save()
                elif self.format == "flac":  # flac
                    # Edit flac tags (artist, thumbnail)
                    audio = FLAC(new_path)
                    audio["ARTIST"] = self.artist  # artist
                    audio["ALBUMARTIST"] = self.artist  # album artist
                    url = yt.thumbnail_url  # derived from youtube_url
                    data = urllib.request.urlopen(url).read()
                    image = Picture()
                    image.data = data
                    audio.add_picture(image)
                    audio.save()
                elif self.format == "mp3":
                    # Edit mp3 tags (artist, thumbnail)
                    audio = EasyID3(new_path)
                    audio["artist"] = self.artist  # artist
                    audio["albumartist"] = self.artist  # album artist
                    audio.save()
                    audio = ID3(new_path)
                    url = yt.thumbnail_url  # derived from youtube_url
                    data = urllib.request.urlopen(url).read()
                    audio["APIC"] = APIC(data=data)
                    audio.save()
            except Exception as e:
                errMsg += f"Tag Error: {e}"

        if errMsg == "":
            self.signal.finish.emit("Success")
        else:
            print(f"Error: {errMsg}")
            self.signal.finish.emit(errMsg)
