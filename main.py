import sys
import os
import webbrowser
import requests
import numpy as np
import pandas as pd
import openpyxl  # required for pd.to_excel()
import time
from pytubefix import YouTube, extract
import urllib.request

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from containers.centralWidget import CentralWidget
from components.queueUnit import QueueUnit

current_version = 'v2.0.2'


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initTheme()
        self.initUI()

    def initTheme(self):
        # Initial Theme Detection
        app = QApplication.instance()
        if app.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            Theme.set_theme("dark")
        else:
            Theme.set_theme("light")
        
        app.setStyleSheet(Theme.get_main_stylesheet())
            
        # Monitor Theme Changes
        app.styleHints().colorSchemeChanged.connect(self.theme_changed)

    def theme_changed(self, scheme: Qt.ColorScheme):
        if scheme == Qt.ColorScheme.Dark:
            Theme.set_theme("dark")
        else:
            Theme.set_theme("light")
        
        QApplication.instance().setStyleSheet(Theme.get_main_stylesheet())
        self.updateTheme()

    def updateTheme(self):
        if hasattr(self, 'central_widget'):
            self.central_widget.updateTheme()

    def initUI(self):
        # layout
        self.showMaximized()
        self.setWindowIcon(QIcon(r'images\icon.ico'))
        self.setWindowTitle("Audio Downloader")
        
        self.menubar()
        # central widget
        self.central_widget = CentralWidget()
        self.setCentralWidget(self.central_widget)

    def menubar(self):
        menubar = self.menuBar()
        # Filemenu
        filemenu = menubar.addMenu("File")

        action_import_xlsx = QAction("Import .xlsx", self)
        action_import_xlsx.triggered.connect(self.import_xlsx_callback)
        action_export_as_xlsx = QAction("Export as .xlsx", self)
        action_export_as_xlsx.triggered.connect(self.export_xlsx_callback)
        filemenu.addActions([action_import_xlsx, action_export_as_xlsx])
        filemenu.addSeparator()

        action_exit = QAction("Exit", self)
        action_exit.triggered.connect(self.exit_callback)
        action_exit.setShortcut("Ctrl+E")
        filemenu.addActions([action_exit])
        # Editmenu
        editmenu = menubar.addMenu("Edit")

        action_delete_all_complete = QAction("Delete all complete", self)
        action_delete_all_complete.triggered.connect(self.delete_all_complete_callback)
        action_delete_all_failed = QAction("Delete all failed", self)
        action_delete_all_failed.triggered.connect(self.delete_all_failed_callback)
        editmenu.addSeparator()

        action_delete_all = QAction("Delete all", self)
        action_delete_all.triggered.connect(self.delete_all_callback)

        editmenu.addActions([action_delete_all_complete, action_delete_all_failed, action_delete_all])
        # Aboutmenu
        aboutmenu = menubar.addMenu("About")

        action_version_info = QAction("Version information", self)
        action_version_info.triggered.connect(self.version_info_callback)
        action_github_repo = QAction("Github repo", self)
        action_github_repo.triggered.connect(self.github_repo_callback)

        aboutmenu.addActions([action_version_info, action_github_repo])
        aboutmenu.addSeparator()

        action_folder_location = QAction("Folder location", self)
        action_folder_location.triggered.connect(self.folder_location_callback)
        aboutmenu.addActions([action_folder_location])

    def import_xlsx_callback(self):
        file = QFileDialog.getOpenFileName(None, "Open a xlsx or csv file...", QDir.homePath(), filter="xlsx(*.xlsx);;csv(*.csv)")[0]  # xlsx

        if not os.path.exists(file):
            pass
        else:
            # load excel data to pddataframe
            root, extension = os.path.splitext(file)
            try:
                if extension == ".xlsx":
                    df = pd.read_excel(file)
                elif extension == ".csv":
                    df = pd.read_csv(file)

                # drop NaN
                df = df.dropna(axis="index", subset=["Youtube URL"], how="any")
                # create units
                self.poolthread = ImportXlsxPoolThread()
                for i in range(len(df)):
                    row = df.iloc[i]
                    work = ImportXlsxThread()
                    work.setRow(row)
                    work.setDeleteUnitMethod(self.central_widget.queueArea.delete_unit_from_list)
                    work.signal.complete.connect(self.__import_xlsx_on_complete)
                    self.poolthread.addThread(work)
                self.poolthread.start()
            except:
                dir = os.path.dirname(file)
                sample_path = os.path.join(dir, "Sample.xlsx")
                sample_data = [["Never Gonna Give You Up", "Rick Astley", "https://youtu.be/dQw4w9WgXcQ"]]
                df = pd.DataFrame(sample_data, columns=["Title", "Artist", "Youtube URL"])
                df.to_excel(sample_path, index=False)
                QMessageBox.warning(self, "Format problem occurs", f"{file}\ncannot be loaded successfully.\n\nModel file is saved to\\{sample_path}.")

    def __import_xlsx_on_complete(self, _props: dict):
        unit = QueueUnit(funcs=[self.central_widget.queueArea.delete_unit_from_list], props=_props)
        self.central_widget.queueArea.render_new_unit(unit)

    def export_xlsx_callback(self):
        dir = QFileDialog.getExistingDirectory(None, "Open destination folder", QDir.homePath())  # 起始路徑
        if dir != "":
            units = self.central_widget.queueArea.get_units()
            data = []
            for unit in units:
                url = unit.getYoutubeURL()
                title = unit.getTitle()
                artist = unit.getArtist()
                data.append([title, artist, url])
            df = pd.DataFrame(data, columns=["Title", "Artist", "Youtube URL"])
            df.to_excel(os.path.join(dir, f"AD_export_{time.time()}.xlsx"), index=False)

    def exit_callback(self):
        sys.exit()

    def delete_all_complete_callback(self):
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() == "COMPLETE":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def delete_all_failed_callback(self):
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() == "FAILED":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def delete_all_callback(self):
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() != "WORKING":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def github_repo_callback(self):
        try:
            webbrowser.open("https://github.com/Xuan-Yi/Audio-Downloader.git")
        except Exception as e:
            QMessageBox.warning(self, "No internet connection", f"Please check your internet connection.\nError------\n{e}")

    def folder_location_callback(self):
        QMessageBox.information(self, "Folder location", os.getcwd())

    def version_info_callback(self):
        try:
            response = requests.get("https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases/latest")
            if response.status_code != 404:
                latest_version = response.json()["tag_name"]
                release_url = str(response.json()["assets"][0]["browser_download_url"])
            else:
                response = requests.get("https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases")
                latest_version = response.json()[0]["tag_name"]
                release_url = response.json()[0]["assets"][0]["browser_download_url"]
            # Current version is given as current_version at top of main.py.
        except Exception as e:
            QMessageBox.warning(self, "No internet connection", f"Please check your internet connection.\nError------\n{e}")

        # Check if is latest version
        isLatestVersion = True
        try:
            current_version_list = str(current_version).split(".")  # convert string to array
            latest_version_list = str(latest_version).split(".")  # convert string to array
            if int(latest_version_list[0].strip("v")) < int(current_version_list[0].strip("v")):
                isLatestVersion = True
            elif int(latest_version_list[1]) < int(current_version_list[1]):
                isLatestVersion = True
            elif int(latest_version_list[2]) < int(current_version_list[2]):
                isLatestVersion = True
            elif latest_version_list == current_version_list:
                isLatestVersion = True
            else:
                isLatestVersion = False
        except Exception as e:
            QMessageBox.warning(None, "No internet connection", f"Please check your internet connection.\nError------\n{e}")

        # Show result
        if isLatestVersion:
            QMessageBox.information(None, "Version informations", f"Current version: {current_version}\nis latest.")
        else:
            reply = QMessageBox.question(
                None, "Version information", f"Latest version: {latest_version}\nCurrent version: {current_version}\nGet latest version?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                webbrowser.open(release_url)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.exit_callback()


class ImportXlsxPoolThread(QThread):
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


class ThreadSignal(QObject):
    complete = pyqtSignal(dict)

    def __init__(self):
        super().__init__()


class ImportXlsxThread(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = ThreadSignal()

    def setRow(self, _row):
        self.url = _row["Youtube URL"]
        self.title = _row["Title"]
        self.artist = _row["Artist"]

    def setDeleteUnitMethod(self, _func):
        self.delete_unit = _func

    def run(self):
        info_dict = dict()
        info_dict["Youtube_obj"] = YouTube(self.url)
        # id
        info_dict["ID"] = extract.video_id(self.url)
        # thumbnail data
        url = info_dict["Youtube_obj"].thumbnail_url
        info_dict["Thumbnail_data"] = urllib.request.urlopen(url).read()
        # title text
        if pd.isnull(self.title):
            title = info_dict["Youtube_obj"].title
            info_dict["Title"] = "".join(x for x in title if x not in '\\/:*?"<>|')
        else:
            info_dict["Title"] = self.title
        # artist text
        if pd.isnull(self.artist):
            artist = info_dict["Youtube_obj"].author
            info_dict["Artist"] = "".join(x for x in artist if x not in '\\/:*?"<>|')
        else:
            info_dict["Artist"] = self.artist
        self.signal.complete.emit(info_dict)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 系統視窗程式
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())  # 偵測視窗關閉後結束程式
