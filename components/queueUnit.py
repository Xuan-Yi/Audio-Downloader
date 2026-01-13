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


class PreviewSlider(QSlider):
    def __init__(self, orientation, time_formatter):
        super().__init__(orientation)
        self._time_formatter = time_formatter

    def _update_value_from_pos(self, pos_x: float):
        width = max(1, self.width())
        ratio = min(max(pos_x / width, 0.0), 1.0)
        value = int(self.minimum() + ratio * (self.maximum() - self.minimum()))
        self.setValue(value)

    def _show_time_tooltip(self, pos_x: float):
        if not self._time_formatter:
            return
        value = self.value()
        text = self._time_formatter(value)
        QToolTip.showText(self.mapToGlobal(QPoint(int(pos_x), -10)), text, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_value_from_pos(event.position().x())
            self._show_time_tooltip(event.position().x())
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self._update_value_from_pos(event.position().x())
            self._show_time_tooltip(event.position().x())
            event.accept()
        super().mouseMoveEvent(event)


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
        print(f"DEBUG: initData1 start for {_url}")
        # youtube object
        self.youtube_obj = YouTube(_url)
        # id
        self.id = extract.video_id(_url)
        # thumbnail data
        url = self.youtube_obj.thumbnail_url  # derived from youtube_url
        print(f"DEBUG: Fetching thumbnail from {url}")
        self.__thumbnail_data = urllib.request.urlopen(url).read()
        # title text
        self.__title_text = self.youtube_obj.title
        self.__title_text = "".join(x for x in self.__title_text if x not in '\\/:*?"<>|')
        # artist text
        self.__artist_text = self.youtube_obj.author
        self.__artist_text = "".join(x for x in self.__artist_text if x not in '\\/:*?"<>|')
        print("DEBUG: initData1 complete")

    def initData2(self, _props: dict):
        self.youtube_obj = _props["Youtube_obj"]
        self.id = _props["ID"]
        self.__thumbnail_data = _props["Thumbnail_data"]
        self.__title_text = _props["Title"]
        self.__artist_text = _props["Artist"]

    def initQt(self):
        print("DEBUG: initQt start")
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
        print("DEBUG: Loading image data into QImage")
        image = QImage()
        image.loadFromData(self.__thumbnail_data)
        pixmap = QPixmap(image).scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        # Crop to square or rounded rect if needed, for now just nice scaling

        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(80, 60)
        self.thumbnail.setPixmap(pixmap)
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setStyleSheet(f"border-radius: 4px; border: 1px solid {Theme.BORDER};")
        self.thumbnail.installEventFilter(self)

        # Play Button Overlay
        self._player_state = "idle"
        self._player_icon_cache = {}
        self.play_btn = QPushButton("", self.thumbnail)
        self.play_btn.setFixedSize(36, 36)
        self.__center_play_button()
        self.play_btn.setIconSize(QSize(18, 18))
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setToolTip("Play Preview")
        self.play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 140);
                color: #ffffff;
                border-radius: 18px;
                font-size: 18px;
                border: 2px solid #ffffff;
                text-align: center;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {Theme.PRIMARY};
                border: 2px solid {Theme.PRIMARY};
            }}
        """)
        self.__apply_player_icon()
        self.play_btn.raise_()
        self.play_btn.clicked.connect(self.__play_preview_callback)
        
        # Connect to player state changes
        try:
            from components.player import preview_player
            preview_player.signals.state_changed.connect(self.__on_player_state_changed)
        except Exception as e:
            print(f"CRITICAL: Failed to connect to preview player: {e}")

        layout.addWidget(self.thumbnail)

        # Info Layout (Vertical: Title, Artist)
        print("DEBUG: Setting up info layout")
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

        # Preview progress bar (visible only while playing)
        self._preview_duration = 0
        try:
            self._preview_duration = int(getattr(self.youtube_obj, "length", 0) or 0)
        except Exception:
            self._preview_duration = 0
        self.preview_progress = PreviewSlider(Qt.Orientation.Horizontal, self.__format_time)
        self.preview_progress.setFixedHeight(12)
        self.preview_progress.setRange(0, max(1, self._preview_duration))
        self.preview_progress.setValue(0)
        self.preview_progress.setTracking(False)
        self.preview_progress.setVisible(False)
        self.preview_progress.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 6px;
                background: {Theme.SECONDARY_PRESSED};
                border: 1px solid {Theme.BORDER};
                border-radius: 3px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Theme.PRIMARY};
                border-radius: 3px;
            }}
            QSlider::add-page:horizontal {{
                background: transparent;
            }}
            QSlider::handle:horizontal {{
                width: 10px;
                margin: -3px 0;
                background: {Theme.TEXT_PRIMARY};
                border-radius: 5px;
            }}
        """)

        self._progress_timer = QTimer(self)
        self._progress_timer.setInterval(250)
        self._progress_timer.timeout.connect(self.__update_preview_progress)
        self._is_seeking = False
        self.preview_progress.sliderPressed.connect(self.__on_preview_seek_pressed)
        self.preview_progress.sliderReleased.connect(self.__on_preview_seek_released)

        info_layout.addWidget(self.preview_progress)

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
        self.setFixedHeight(112)  # Slightly taller to fit preview progress bar
        self.setMinimumWidth(380) # Ensure content fits horizontally

    def eventFilter(self, source, event):
        if source is self.thumbnail and event.type() == QEvent.Type.Resize:
            self.__center_play_button()
        return super().eventFilter(source, event)

    def __center_play_button(self):
        x = (self.thumbnail.width() - self.play_btn.width()) // 2
        y = (self.thumbnail.height() - self.play_btn.height()) // 2
        self.play_btn.move(x, y)

    def __build_player_icon(self, state: str) -> QIcon:
        size = 18
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#ffffff"))

        if state == "play":
            points = QPolygonF([
                QPointF(size * 0.30, size * 0.20),
                QPointF(size * 0.30, size * 0.80),
                QPointF(size * 0.80, size * 0.50),
            ])
            painter.drawPolygon(points)
        elif state == "pause":
            bar_width = size * 0.22
            gap = size * 0.12
            left = (size - (2 * bar_width + gap)) / 2
            top = size * 0.20
            height = size * 0.60
            painter.drawRoundedRect(QRectF(left, top, bar_width, height), 1.5, 1.5)
            painter.drawRoundedRect(QRectF(left + bar_width + gap, top, bar_width, height), 1.5, 1.5)
        painter.end()
        return QIcon(pixmap)

    def __apply_player_icon(self):
        icon_state = "pause" if self._player_state in ("playing", "buffering") else "play"

        if icon_state not in self._player_icon_cache:
            self._player_icon_cache[icon_state] = self.__build_player_icon(icon_state)

        self.play_btn.setIcon(self._player_icon_cache[icon_state])

    def __set_player_state(self, state: str):
        self._player_state = state
        self.__apply_player_icon()

    def __delete_callback(self):
        try:
            from components.player import preview_player
            preview_player.stop()
        except:
            pass
        self.delete_unit_from_list(self.id)

    def __play_preview_callback(self):
        from components.player import preview_player
        preview_player.toggle(self.id, self.url)

    def __on_player_state_changed(self, video_id, state):
        if video_id == self.id:
            if state == "playing":
                self.__set_player_state("playing")
                self.play_btn.setToolTip("Pause Preview")
                self.preview_progress.setEnabled(True)
                self.__start_progress()
            elif state == "buffering":
                self.__set_player_state("buffering")
                self.play_btn.setToolTip("Pause Preview")
                self.preview_progress.setEnabled(False)
                self.__stop_progress(hide=True)
            else:
                self.__set_player_state("paused")
                self.play_btn.setToolTip("Play Preview")
                self.preview_progress.setEnabled(True)
                self.__stop_progress(hide=True)
        else:
            self.__set_player_state("idle")
            self.play_btn.setToolTip("Play Preview")
            self.preview_progress.setEnabled(True)
            self.__stop_progress(hide=True)

    def __start_progress(self):
        if self._preview_duration <= 0:
            return
        self.preview_progress.setVisible(True)
        if not self._progress_timer.isActive():
            self._progress_timer.start()
        self.__update_preview_progress()

    def __stop_progress(self, hide: bool = False):
        if self._progress_timer.isActive():
            self._progress_timer.stop()
        if hide:
            self.preview_progress.setVisible(False)
        self.preview_progress.setValue(0)

    def __format_time(self, seconds: int) -> str:
        total = max(0, int(seconds))
        hours = total // 3600
        minutes = (total % 3600) // 60
        secs = total % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"

    def __update_preview_progress(self):
        if self._is_seeking:
            return
        try:
            from components.player import preview_player
            pos = preview_player.get_playback_position(self.id)
        except Exception:
            pos = None
        if pos is None:
            return
        if self._preview_duration > 0:
            value = int(min(max(pos, 0.0), self._preview_duration))
            self.preview_progress.setValue(value)

    def __on_preview_seek_pressed(self):
        self._is_seeking = True
        if self._progress_timer.isActive():
            self._progress_timer.stop()

    def __on_preview_seek_released(self):
        if self._preview_duration <= 0:
            return
        try:
            from components.player import preview_player
            pos = preview_player.get_playback_position(self.id)
        except Exception:
            pos = None

        if self._player_state == "buffering":
            if pos is not None:
                self.preview_progress.setValue(int(min(max(pos, 0.0), self._preview_duration)))
            self._is_seeking = False
            if self.preview_progress.isVisible():
                self._progress_timer.start()
            return

        seek_to = float(self.preview_progress.value())
        try:
            from components.player import preview_player
            preview_player.seek(self.id, self.url, seek_to)
        except Exception:
            pass
        self._is_seeking = False
        if self.preview_progress.isVisible():
            self._progress_timer.start()

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
        self.play_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 150);
                color: white;
                border-radius: 15px;
                font-size: 14px;
                border: none;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {Theme.PRIMARY};
            }}
        """)
        self._player_icon_cache.clear()
        self.__apply_player_icon()
        self.title.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_PRIMARY}; font-weight: bold; font-size: 11pt;")
        self.artist.setStyleSheet(f"border: none; background: transparent; color: {Theme.TEXT_SECONDARY}; font-size: 10pt;")
        self.preview_progress.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                height: 6px;
                background: {Theme.SECONDARY_PRESSED};
                border: 1px solid {Theme.BORDER};
                border-radius: 3px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Theme.PRIMARY};
                border-radius: 3px;
            }}
            QSlider::add-page:horizontal {{
                background: transparent;
            }}
            QSlider::handle:horizontal {{
                width: 10px;
                margin: -3px 0;
                background: {Theme.TEXT_PRIMARY};
                border-radius: 5px;
            }}
        """)
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

        m4a_exists_before = False
        try:
            # download returns the file path
            stream = yt.streams.get_audio_only()
            if stream is None:
                # Fallback: try filtering manually
                stream = yt.streams.filter(only_audio=True).first()

            if stream:
                # Check if file exists before downloading
                expected_filename = stream.default_filename
                expected_path = os.path.join(self.dir, expected_filename)
                if os.path.exists(expected_path):
                    m4a_exists_before = True
                    original_path = expected_path
                else:
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
                        if not m4a_exists_before:
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

        # Recover/Tag original m4a if preserved
        if errMsg == "" and os.path.exists(original_path) and original_path.endswith(".m4a") and os.path.abspath(original_path) != os.path.abspath(new_path):
            try:
                audio = MP4(original_path)
                audio["\xa9ART"] = self.artist  # artist
                audio["aART"] = self.artist  # album artist
                url = yt.thumbnail_url  # derived from youtube_url
                data = urllib.request.urlopen(url).read()
                audio["covr"] = [MP4Cover(data, imageformat=MP4Cover.FORMAT_JPEG)]
                audio.save()
            except Exception as e:
                print(f"Warning: Could not tag original M4A: {e}")

        if errMsg == "":
            self.signal.finish.emit("Success")
        else:
            print(f"Error: {errMsg}")
            self.signal.finish.emit(errMsg)
