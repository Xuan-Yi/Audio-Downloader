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
import tomllib
from pathlib import Path

def get_app_version():
    try:
        pyproject_path = Path(__file__).parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            return f"v{data['project']['version']}"
    except Exception:
        return 'v0.0.0'

current_version = get_app_version()


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
        self.setMinimumWidth(440) # Ensure content fits horizontally
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
        filePath, _ = QFileDialog.getOpenFileName(self, "Import Music List", QDir.homePath(), "Excel files (*.xlsx);;CSV files (*.csv)")

        if not filePath:
            return

        try:
            if filePath.endswith('.xlsx'):
                df = pd.read_excel(filePath)
            elif filePath.endswith('.csv'):
                df = pd.read_csv(filePath)
            else:
                QMessageBox.warning(self, "Unsupported File", f"The file {os.path.basename(filePath)} is not a supported format. Please use .xlsx or .csv.")
                return

            if "Youtube URL" not in df.columns:
                raise ValueError("The file must contain a 'Youtube URL' column.")

            df = df.dropna(axis="index", subset=["Youtube URL"], how="any")

            self.poolthread = ImportXlsxPoolThread()
            for i in range(len(df)):
                row = df.iloc[i]
                work = ImportXlsxThread()
                work.setRow(row)
                work.setDeleteUnitMethod(self.central_widget.queueArea.delete_unit_from_list)
                work.signal.complete.connect(self.__import_xlsx_on_complete)
                self.poolthread.addThread(work)
            self.poolthread.start()
        except Exception as e:
            dir = os.path.dirname(filePath)
            sample_path = os.path.join(dir, "Sample.xlsx")
            sample_data = [["Never Gonna Give You Up", "Rick Astley", "https://youtu.be/dQw4w9WgXcQ"]]
            df_sample = pd.DataFrame(sample_data, columns=["Title", "Artist", "Youtube URL"])
            try:
                df_sample.to_excel(sample_path, index=False)
                QMessageBox.warning(self, "Import Error", f"'{os.path.basename(filePath)}' could not be loaded.\n\nA sample file has been created at:\n{sample_path}\n\nError: {e}")
            except Exception as sample_e:
                QMessageBox.warning(self, "Import Error", f"'{os.path.basename(filePath)}' could not be loaded and a sample file could not be created.\n\nImport Error: {e}\nSample Creation Error: {sample_e}")

    def __import_xlsx_on_complete(self, _props: dict):
        unit = QueueUnit(funcs=[self.central_widget.queueArea.delete_unit_from_list], props=_props)
        self.central_widget.queueArea.render_new_unit(unit)

    def export_xlsx_callback(self):
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        suggested_filename = f"AudioDownloader_export_{current_time}.xlsx"

        filePath, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export As",
            os.path.join(QDir.homePath(), suggested_filename),
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )

        if filePath:
            units = self.central_widget.queueArea.get_units()
            data = []
            for unit in units:
                url = unit.getYoutubeURL()
                title = unit.getTitle()
                artist = unit.getArtist()
                data.append([title, artist, url])

            df = pd.DataFrame(data, columns=["Title", "Artist", "Youtube URL"])

            try:
                if '(*.xlsx)' in selected_filter:
                    df.to_excel(filePath, index=False)
                elif '(*.csv)' in selected_filter:
                    df.to_csv(filePath, index=False)
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"Could not save file to '{filePath}'.\n\nError: {e}")

    def exit_callback(self):
        sys.exit()

    def delete_all_complete_callback(self):
        from components.player import preview_player
        preview_player.stop()
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() == "COMPLETE":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def delete_all_failed_callback(self):
        from components.player import preview_player
        preview_player.stop()
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() == "FAILED":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def delete_all_callback(self):
        from components.player import preview_player
        preview_player.stop()
        units = self.central_widget.queueArea.get_units()
        ids = []
        for unit in units:
            if unit.getState() != "WORKING":
                ids.append(unit.getID())
        for id in ids:
            self.central_widget.queueArea.delete_unit_from_list(id)

    def github_repo_callback(self):
        reply = QMessageBox.question(
            self, "Open GitHub Repository", 
            "Would you like to open the GitHub repository in your browser?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                webbrowser.open("https://github.com/Xuan-Yi/Audio-Downloader.git")
            except Exception as e:
                QMessageBox.warning(self, "No internet connection", f"Please check your internet connection.\nError------\n{e}")

    def folder_location_callback(self):
        QMessageBox.information(self, "Folder location", os.getcwd())

    def version_info_callback(self):
        latest_version = None
        release_url = None

        try:
            response = requests.get("https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases/latest")
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name")
                if data.get("assets"):
                    release_url = data["assets"][0].get("browser_download_url")
            else:
                response = requests.get("https://api.github.com/repos/Xuan-Yi/Audio-Downloader/releases")
                if response.status_code == 200 and len(response.json()) > 0:
                    data = response.json()[0]
                    latest_version = data.get("tag_name")
                    if data.get("assets"):
                        release_url = data["assets"][0].get("browser_download_url")
        except Exception as e:
            QMessageBox.warning(self, "Network Error", f"Could not check for updates.\nError: {e}")
            return

        if not latest_version:
            QMessageBox.information(self, "Version information", f"Current version: {current_version}\nNo remote version found.")
            return

        # Check if is latest version
        try:
            def parse_version(v):
                return tuple(map(int, v.strip("v").split(".")))

            current_v = parse_version(current_version)
            latest_v = parse_version(latest_version)
            
            isLatestVersion = current_v >= latest_v
        except Exception as e:
            QMessageBox.warning(None, "Version check error", f"Could not compare versions.\nError: {e}")
            return

        # Show result
        if isLatestVersion:
            QMessageBox.information(None, "Version informations", f"Current version: {current_version}\nis latest.")
        else:
            msg = f"Latest version: {latest_version}\nCurrent version: {current_version}"
            if release_url:
                reply = QMessageBox.question(
                    None, "Update Available", f"{msg}\n\nGet latest version?", 
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    webbrowser.open(release_url)
            else:
                QMessageBox.information(None, "Update Available", f"{msg}\n\nPlease check the GitHub repository for the release.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.exit_callback()

    def closeEvent(self, event):
        try:
            from components.player import preview_player
            preview_player.force_stop_all()
        except:
            pass
        event.accept()


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
        self.title = _row.get("Title")
        self.artist = _row.get("Artist")

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
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys.__excepthook__(exctype, value, traceback)
    sys.excepthook = exception_hook

    app = QApplication(sys.argv)  # 系統視窗程式
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())  # 偵測視窗關閉後結束程式
