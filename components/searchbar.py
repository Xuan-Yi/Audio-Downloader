from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme


class SearchBar(QWidget):
    def __init__(self, funcs: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.create_unit] = funcs

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Search Input
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Paste YouTube URL here...")
        self.searchbar.setToolTip("Press Enter or click Add")
        self.searchbar.setFixedHeight(42)

        # Add Button
        self.add_btn = QPushButton("Add")
        self.add_btn.setFixedSize(80, 42)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.setStyleSheet(Theme.button_primary())
        self.add_btn.clicked.connect(self.on_add_clicked)

        layout.addWidget(self.searchbar, 1)  # Stretch factor 1
        layout.addWidget(self.add_btn)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.on_add_clicked()

    def on_add_clicked(self):
        url = str(self.searchbar.text()).strip()
        if url:
            error = self.create_unit(url)
            self.searchbar.setText("")
            if error:
                # Show a non-blocking tooltip near the searchbar
                QToolTip.showText(self.searchbar.mapToGlobal(QPoint(0, self.searchbar.height())), error, self.searchbar)

    def setDisabled(self, disable: bool):
        self.searchbar.setDisabled(disable)
        self.add_btn.setDisabled(disable)

    def updateTheme(self):
        self.add_btn.setStyleSheet(Theme.button_primary())
