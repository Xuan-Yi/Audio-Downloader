from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components.lines import *
from components.queueUnit import QueueUnit

from pytube import YouTube


class ScrollQueue(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = []

        self.font = QFont('Segoe UI', 11)
        self.setWidgetResizable(True)
        self.setStyleSheet("border: transparent;")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.showFullScreen()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        pwgt = QWidget()
        # something should be added to layout
        pwgt.setLayout(layout)
        self.setWidget(pwgt)
        self.setMinimumWidth(pwgt.sizeHint().width()+100)
        self.setMaximumHeight(pwgt.sizeHint().height())

    def create_unit(self, url: str):
        exist = False
        youtube_obj = ''
        try:
            youtube_obj = YouTube(url)
            for unit in self.units:
                if unit.getYoutubeObj() == youtube_obj:
                    exist = True
        except Exception as e:
            QMessageBox.warning(None, "URL warning",
                                f"URL is not valid.\nError message------\n{e}")

        if not exist:
            if youtube_obj != '':
                try:
                    new_unit = QueueUnit(youtube_url=url, funcs=[
                                         self.delete_unit_from_list])
                    self.units.append(new_unit)
                    self.render_list()
                    return new_unit
                except Exception as e:
                    QMessageBox.warning(
                        None, "URL warning", f"URL is not valid.\nError message------\n{e}")
        else:
            QMessageBox.information(
                None, "Duplicate source", "This song has existed.")

    def render_new_unit(self,unit:QueueUnit):
        self.units.append(unit)
        self.render_list()
    
    def render_list(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        pwgt = QWidget()

        for unit in self.units:
            layout.addWidget(unit)

        pwgt.setLayout(layout)
        self.setWidget(pwgt)
        self.setMinimumWidth(pwgt.sizeHint().width()+100)
        self.setMaximumHeight(pwgt.sizeHint().height())

    def delete_unit_from_list(self, id: str):
        for unit in self.units:
            if unit.getID() == id:
                self.units.remove(unit)
                unit.deleteLater()
        self.render_list()    # rerender all

    def get_units(self):
        return self.units
