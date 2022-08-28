from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from components.lines import *
from components.searchbar import SearchBar
from components.infoarea import Infoarea

shadowEffect = QGraphicsDropShadowEffect()
shadowEffect.setBlurRadius(12)
shadowEffect.setOffset(0, 0)
shadowEffect.setColor(QColor(0, 0, 0, 100))


class SettingArea(QWidget):
    def __init__(self, funcs: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.create_unit, self.setInfos, self.convert] = funcs

        self.font = QFont('Segoe UI', 11)
        self.setContentsMargins(40, 6, 40, 6)
        self.setFixedHeight(280)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(12)

        self.searchbar = SearchBar(funcs=[self.create_unit])
        self.infoarea = Infoarea(funcs=[self.setInfos])
        # covert button
        self.convert_btn = QPushButton(text='Convert', font=self.font)
        self.convert_btn.setFixedHeight(32)
        self.convert_btn.setStyleSheet(
            'QPushButton {border-radius: 12px; background-color: white; padding: 1px; }'
            'QPushButton::hover {background-color: #d9d9d9; }'
            'QPushButton::pressed {background-color: #e6e6e6;}')
        self.convert_btn.setGraphicsEffect(shadowEffect)
        self.convert_btn.clicked.connect(self.onConvertBtnClicked)
        self.layout.addWidget(self.searchbar)
        self.layout.addWidget(self.infoarea)
        self.layout.addWidget(self.convert_btn)
        self.setLayout(self.layout)

    def onConvertBtnClicked(self):
        # start convert
        self.convert()
