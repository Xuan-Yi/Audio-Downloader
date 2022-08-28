from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

shadowEffect = QGraphicsDropShadowEffect()
shadowEffect.setBlurRadius(6)
shadowEffect.setOffset(0,0)
shadowEffect.setColor(QColor(0,0,0,100))

class SearchBar(QWidget):
    def __init__(self,funcs:list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        [self.create_unit] = funcs
        
        self.font = QFont('Segoe UI', 11)    
        layout = QGridLayout()
        layout.setSpacing(12)
        
        # label
        self.label = QLabel(font = self.font,text='Youtbe URL')
        self.label.setAlignment(Qt.AlignRight)
        self.label.setFixedHeight(32)
        layout.addWidget(self.label,0,0,1,1)
        # searchbar
        self.searchbar = QLineEdit(font = self.font)
        self.searchbar.setPlaceholderText('Youtube URL')
        self.searchbar.setFixedHeight(self.label.sizeHint().height())
        self.searchbar.setMinimumWidth(400)
        self.searchbar.setGraphicsEffect(shadowEffect)
        self.searchbar.setAlignment(Qt.AlignLeft)
        self.searchbar.setStyleSheet('border-radius: 12px;  padding: 2px 8px;')
        layout.addWidget(self.searchbar,0,1,1,6)
        
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            url = str(self.searchbar.text())
            self.searchbar.setText("")
            self.create_unit(url)
    
    def setDisabled(self,disable:bool):
        self.searchbar.setDisabled(disable)
            
            
    