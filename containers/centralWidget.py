from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components.lines import *
from containers.SettingArea import SettingArea
from containers.ScrollArea import ScrollQueue


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font = QFont('Segoe UI', 11)
        self.initUI()

    def initUI(self):
        [self.format, self.dir] = ['flac', QDir.homePath()]

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(12)
        # subwidgets
        self.queueArea = ScrollQueue()
        self.settingArea = SettingArea(
            funcs=[self.queueArea.create_unit, self.setInfos, self.convert])
        HLine = QHLine()

        self.layout.addWidget(self.settingArea)
        self.layout.addWidget(HLine)
        self.layout.addWidget(self.queueArea)
        self.setLayout(self.layout)

    def setInfos(self, format: str, dir: str):
        self.format, self.dir = format, dir

    def convert(self):
        self.poolthread = DownloadPoolThread()
        self.poolthread.complete.connect(self.__on_convert_complete)
        units = self.queueArea.get_units()
        for unit in units:
            if unit.getState() in ['WAITING', 'COMPLETE', 'FAILED']:
                unit.createThread(self.dir, self.format)
                thread = unit.getThread()
                self.poolthread.addThread(thread)
        self.poolthread.start()
        self.settingArea.infoarea.setDisabled(True)
        self.settingArea.convert_btn.setDisabled(True)

    def __on_convert_complete(self):
        self.settingArea.infoarea.setDisabled(False)
        self.settingArea.convert_btn.setDisabled(False)


class DownloadPoolThread(QThread):
    # Thread to manage thread pool
    trigger = pyqtSignal(int)   # progress
    complete = pyqtSignal()
    thread_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threadpool = QThreadPool()
        maxThreadCount = 12  # maximum thread number
        self.threadpool.setMaxThreadCount(maxThreadCount)

    def addThread(self, _thread):
        self.thread_list.append(_thread)

    def run(self):
        for t in self.thread_list:
            self.threadpool.start(t)
        self.threadpool.waitForDone()
        self.thread_list.clear()
        self.complete.emit()
