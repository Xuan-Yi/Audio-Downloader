from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

from components.searchbar import SearchBar
from components.infoarea import Infoarea

class SettingArea(QWidget):
    def __init__(self, funcs: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.create_unit, self.setInfos, self.convert] = funcs

        self.setContentsMargins(20, 20, 20, 10)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)

        # Search Section
        self.searchbar = SearchBar(funcs=[self.create_unit])
        
        # Options Section (Info Area)
        self.infoarea = Infoarea(funcs=[self.setInfos])
        
        # Action Section (Download Button)
        self.convert_btn = QPushButton(text='Download All')
        self.convert_btn.setFixedHeight(42)
        self.convert_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.convert_btn.setStyleSheet(Theme.button_primary())
        self.convert_btn.setFont(QFont(Theme.FONT_FAMILY, 11, QFont.Weight.Bold))
        self.convert_btn.clicked.connect(self.onConvertBtnClicked)
        
        self.layout.addWidget(self.searchbar)
        self.layout.addWidget(self.infoarea)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.convert_btn)
        
        self.setLayout(self.layout)

    def onConvertBtnClicked(self):
        # start convert
        self.convert()

    def updateTheme(self):
        self.searchbar.updateTheme()
        self.infoarea.updateTheme()
        self.convert_btn.setStyleSheet(Theme.button_primary())
