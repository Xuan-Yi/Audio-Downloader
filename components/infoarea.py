from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.styles import Theme

formats = ['flac','mp3','m4a','wav']

class ElidedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._full_text = text
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)

    def setText(self, text):
        self._full_text = text
        super().setText(text) # Keep internal state for accessibility/tooltips
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self._full_text, Qt.TextElideMode.ElideMiddle, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)

class Infoarea(QWidget):
    def __init__(self, funcs: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.setInfos] = funcs
        
        self.output_format = 'flac'
        self.dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
        
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        # Format Selection Group
        format_layout = QHBoxLayout()
        self.label = QLabel('Format:')
        self.label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-weight: 500;")
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(formats)
        self.format_combo.setFixedWidth(80)
        self.format_combo.setCurrentText(formats[0])
        self.format_combo.currentIndexChanged.connect(self.__format_combo_change_callback)
        self.format_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        
        format_layout.addWidget(self.label)
        format_layout.addWidget(self.format_combo)

        # Directory Selection Group
        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(10)
        
        self.openFolderBtn = QPushButton('Choose Folder')
        self.openFolderBtn.setStyleSheet(Theme.button_secondary())
        self.openFolderBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.openFolderBtn.clicked.connect(self.__open_folder_callback)
        
        self.dirT = ElidedLabel(f'{self.dir}')
        self.dirT.setStyleSheet(f'color: {Theme.TEXT_SECONDARY}; font-style: italic;')
        # No need to set word wrap or manually elide
        
        dir_layout.addWidget(self.openFolderBtn)
        dir_layout.addWidget(self.dirT, 1)

        layout.addLayout(format_layout)
        layout.addLayout(dir_layout, 1) # Give directory section more space
        
        self.setLayout(layout)

    def __format_combo_change_callback(self):
        self.output_format = self.format_combo.currentText()
        self.setInfos(format=self.output_format, dir=self.dir)
        
    def __open_folder_callback(self):
        dir = QFileDialog.getExistingDirectory(None, "Open destination folder", QDir.homePath())
        if dir != "":
            self.dir = dir
            self.dirT.setText(dir)
            self.dirT.setToolTip(dir)
        self.setInfos(format=self.output_format, dir=self.dir)
        
    def getFormat(self):
        return self.output_format
    
    def getdir(self):
        return self.dir
    
    def setDisabled(self, disable: bool):
        self.format_combo.setDisabled(disable)
        self.openFolderBtn.setDisabled(disable)

    def updateTheme(self):
        self.label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-weight: 500;")
        self.dirT.setStyleSheet(f'color: {Theme.TEXT_SECONDARY}; font-style: italic;')
        self.openFolderBtn.setStyleSheet(Theme.button_secondary())
    