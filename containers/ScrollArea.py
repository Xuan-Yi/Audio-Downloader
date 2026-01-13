from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from components.queueUnit import QueueUnit

from pytubefix import YouTube, extract
import urllib.request
import pandas as pd


class ThreadSignal(QObject):
    complete = pyqtSignal(dict)

    def __init__(self):
        super().__init__()


class FetchInfoThread(QRunnable):
    def __init__(self, url, title=None, artist=None):
        super().__init__()
        self.url = url
        self.title = title
        self.artist = artist
        self.signal = ThreadSignal()

    def run(self):
        try:
            info_dict = dict()
            info_dict["Youtube_obj"] = YouTube(self.url)
            # id
            info_dict["ID"] = extract.video_id(self.url)
            # thumbnail data
            url = info_dict["Youtube_obj"].thumbnail_url
            info_dict["Thumbnail_data"] = urllib.request.urlopen(url).read()
            # title text
            if pd.isnull(self.title) or self.title is None:
                title = info_dict["Youtube_obj"].title
                info_dict["Title"] = "".join(x for x in title if x not in '\\/:*?"<>|')
            else:
                info_dict["Title"] = self.title
            # artist text
            if pd.isnull(self.artist) or self.artist is None:
                artist = info_dict["Youtube_obj"].author
                info_dict["Artist"] = "".join(x for x in artist if x not in '\\/:*?"<>|')
            else:
                info_dict["Artist"] = self.artist
            self.signal.complete.emit(info_dict)
        except Exception as e:
            print(f"Error fetching info for {self.url}: {e}")


class ScrollQueue(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = []
        self.thread_pool = QThreadPool.globalInstance()
        # ... rest of init remains same ...

        self.setWidgetResizable(True)
        self.setStyleSheet(Theme.get_main_stylesheet())  # Apply global/scroll styles
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setMinimumHeight(120)  # Ensure at least one unit is visible
        self.initUI()

    def initUI(self):
        self.content_widget = QWidget()
        self.content_widget.setMinimumWidth(400)  # Ensure units have enough horizontal space
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.content_widget.setLayout(self.content_layout)
        self.setWidget(self.content_widget)

    def create_unit(self, url: str, title: str = None, artist: str = None, silent: bool = False):
        url = url.strip()
        if not url:
            return None

        exist = False
        video_id = ""
        try:
            video_id = extract.video_id(url)
            for unit in self.units:
                if unit.getID() == video_id:
                    exist = True
                    break
        except Exception as e:
            err_msg = f"URL is not valid.\n{e}"
            if not silent:
                print(f"Warning: {err_msg}")
            return err_msg

        if exist:
            return "This song has existed in queue."

        # Start background fetch
        worker = FetchInfoThread(url, title, artist)
        worker.signal.complete.connect(self.render_new_unit_from_props)
        self.thread_pool.start(worker)
        return None

    def render_new_unit_from_props(self, props: dict):
        # Double check existence again to handle race conditions
        for u in self.units:
            if u.getID() == props["ID"]:
                return

        new_unit = QueueUnit(funcs=[self.delete_unit_from_list], props=props)
        self.units.append(new_unit)
        self.render_list()

    def render_new_unit(self, unit: QueueUnit):
        # Prevent duplicates
        for u in self.units:
            if u.getID() == unit.getID():
                return
        self.units.append(unit)
        self.render_list()

    def render_list(self):
        # Clear existing items from layout without deleting objects
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        # Re-add all units
        for unit in self.units:
            self.content_layout.addWidget(unit)

    def delete_unit_from_list(self, id: str):
        for unit in self.units:
            if unit.getID() == id:
                self.units.remove(unit)
                unit.deleteLater()
        self.render_list()  # rerender all

    def get_units(self):
        return self.units

    def updateTheme(self):
        self.setStyleSheet(Theme.get_main_stylesheet())
        for unit in self.units:
            unit.updateTheme()
