from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

formats = ['flac','mp3','m4a','wav']
format_map = {'m4a': 'mp4', 'mp3': 'mp3', 'wav': 'wav', 'flac': 'flac'}

shadowEffect = QGraphicsDropShadowEffect()
shadowEffect.setBlurRadius(6)
shadowEffect.setOffset(0,0)
shadowEffect.setColor(QColor(0,0,0,100))


class Infoarea(QWidget):
    def __init__(self,funcs:list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.setInfos] = funcs
        
        self.font = QFont('Segoe UI', 11)
        layout = QGridLayout()
        layout.setSpacing(12)
        
        self.output_format = 'flac'
        self.dir = QDir.homePath()
        
        # audio format combobox
        self.label = QLabel(font = self.font,text='Audio format')
        self.label.setAlignment(Qt.AlignRight)
        self.format_combo = QComboBox()
        self.format_combo.addItems(formats)
        self.format_combo.setFont(self.font)
        self.format_combo.setCurrentText(formats[0])
        self.format_combo.currentIndexChanged.connect(self.__format_combo_change_callback)
        layout.addWidget(self.label,0,0,1,1)
        layout.addWidget(self.format_combo,0,1,1,2)
        # dir
        self.openFolderBtn = QPushButton(text='Open Folder',font = self.font)    # choose folder
        self.openFolderBtn.setStyleSheet(
            'QPushButton {border-radius: 12px; background-color: white; padding: 1px; }'
            'QPushButton::hover {background-color: #d9d9d9; }'
            'QPushButton::pressed {background-color: #e6e6e6;}')
        self.openFolderBtn.setGraphicsEffect(shadowEffect)
        self.openFolderBtn.setFixedSize(175, 32)
        self.openFolderBtn.clicked.connect(self.__open_folder_callback)
        layout.addWidget(self.openFolderBtn, 0, 3, 1, 1)
        self.dirT = QLabel(text=f'{self.dir}')  # folder name showcase
        self.dirT.setStyleSheet('background-color: rgba(0,0,0,0.03); padding: 2px;')
        self.dirT.setFont(self.font)
        self.dirT.setFixedHeight(32)
        layout.addWidget(self.dirT, 0, 4, 1, 6)
        
        self.setLayout(layout)

    def __format_combo_change_callback(self):
        self.output_format = self.format_combo.currentText()
        self.setInfos(format =self.output_format,dir = self.dir)
        
    def __open_folder_callback(self):
        dir = QFileDialog.getExistingDirectory(None, "Open destination folder", QDir.homePath())   # 起始路徑
        if dir != "":
            self.dir = dir
            self.dirT.setText(dir)
        self.setInfos(format =self.output_format,dir = self.dir)
        
    def getFormat(self):
        return self.output_format
    
    def getdir(self):
        return self.dir
    
    def setDisabled(self,disable:bool):
        self.format_combo.setDisabled(disable)
        self.openFolderBtn.setDisabled(disable)
            
    