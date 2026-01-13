from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from containers.SettingArea import SettingArea
from containers.ScrollArea import ScrollQueue


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        [self.format, self.dir] = ['flac', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)]

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # subwidgets
        self.queueArea = ScrollQueue()
        self.settingArea = SettingArea(
            funcs=[self.queueArea.create_unit, self.setInfos, self.convert])
        
        # Add a subtle separator or just rely on spacing/colors
        # Using a QFrame line from lines.py, but maybe styled differently?
        # Let's keep it clean, maybe a shadow or border on the SettingArea bottom?
        # For now, just add them directly.
        
        self.layout.addWidget(self.settingArea)
        
        # Divider line
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setStyleSheet(f"color: {Theme.BORDER}; background-color: {Theme.BORDER}; border: none; max-height: 1px;")
        self.layout.addWidget(self.line)
        
        self.layout.addWidget(self.queueArea)
        self.setLayout(self.layout)

    def updateTheme(self):
        self.settingArea.updateTheme()
        self.queueArea.updateTheme()
        self.line.setStyleSheet(f"color: {Theme.BORDER}; background-color: {Theme.BORDER}; border: none; max-height: 1px;")

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
        self.settingArea.searchbar.setDisabled(True)

    def __on_convert_complete(self):
        self.settingArea.infoarea.setDisabled(False)
        self.settingArea.convert_btn.setDisabled(False)
        self.settingArea.searchbar.setDisabled(False)


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
