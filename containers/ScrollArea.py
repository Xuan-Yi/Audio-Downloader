from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from components.queueUnit import QueueUnit

from pytubefix import YouTube


class ScrollQueue(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = []

        self.setWidgetResizable(True)
        self.setStyleSheet(Theme.get_main_stylesheet()) # Apply global/scroll styles
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setMinimumHeight(120) # Ensure at least one unit is visible
        self.initUI()

    def initUI(self):
        self.content_widget = QWidget()
        self.content_widget.setMinimumWidth(400) # Ensure units have enough horizontal space
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.content_widget.setLayout(self.content_layout)
        self.setWidget(self.content_widget)

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
        self.render_list()    # rerender all

    def get_units(self):
        return self.units

    def updateTheme(self):
        self.setStyleSheet(Theme.get_main_stylesheet())
        for unit in self.units:
            unit.updateTheme()
