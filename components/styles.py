from PyQt6.QtGui import QColor, QPalette

class Theme:
    # Default to Light Theme values initially
    PRIMARY = "#3b82f6"
    PRIMARY_HOVER = "#2563eb"
    PRIMARY_PRESSED = "#1d4ed8"
    
    SECONDARY = "#ffffff"
    SECONDARY_HOVER = "#f3f4f6"
    SECONDARY_PRESSED = "#e5e7eb"
    
    BACKGROUND = "#f9fafb"
    SURFACE = "#ffffff"
    
    TEXT_PRIMARY = "#111827"
    TEXT_SECONDARY = "#6b7280"
    
    BORDER = "#e5e7eb"
    
    ERROR = "#ef4444"
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"

    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_MAIN = 10
    FONT_SIZE_LARGE = 11

    @classmethod
    def set_theme(cls, mode: str):
        if mode == "dark":
            cls.PRIMARY = "#60a5fa"        # Lighter blue for dark mode
            cls.PRIMARY_HOVER = "#3b82f6"
            cls.PRIMARY_PRESSED = "#2563eb"
            
            cls.SECONDARY = "#1f2937"      # Dark gray
            cls.SECONDARY_HOVER = "#374151"
            cls.SECONDARY_PRESSED = "#4b5563"
            
            cls.BACKGROUND = "#111827"     # Very dark blue/gray
            cls.SURFACE = "#1f2937"        # Dark gray surface
            
            cls.TEXT_PRIMARY = "#f9fafb"   # White text
            cls.TEXT_SECONDARY = "#9ca3af" # Light gray text
            
            cls.BORDER = "#374151"         # Darker border
            
            cls.ERROR = "#f87171"          # Lighter red
            cls.SUCCESS = "#34d399"        # Lighter green
            cls.WARNING = "#fbbf24"        # Lighter yellow
        else:
            # Light Theme (Reset to defaults)
            cls.PRIMARY = "#3b82f6"
            cls.PRIMARY_HOVER = "#2563eb"
            cls.PRIMARY_PRESSED = "#1d4ed8"
            
            cls.SECONDARY = "#ffffff"
            cls.SECONDARY_HOVER = "#f3f4f6"
            cls.SECONDARY_PRESSED = "#e5e7eb"
            
            cls.BACKGROUND = "#f9fafb"
            cls.SURFACE = "#ffffff"
            
            cls.TEXT_PRIMARY = "#111827"
            cls.TEXT_SECONDARY = "#6b7280"
            
            cls.BORDER = "#e5e7eb"
            
            cls.ERROR = "#ef4444"
            cls.SUCCESS = "#10b981"
            cls.WARNING = "#f59e0b"

    @staticmethod
    def get_main_stylesheet():
        return f"""
            QMainWindow {{
                background-color: {Theme.BACKGROUND};
            }}
            QWidget {{
                font-family: "{Theme.FONT_FAMILY}";
                font-size: {Theme.FONT_SIZE_MAIN}pt;
                color: {Theme.TEXT_PRIMARY};
            }}
            QLineEdit {{
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                color: {Theme.TEXT_PRIMARY};
                selection-background-color: {Theme.PRIMARY};
                selection-color: {Theme.SURFACE};
            }}
            QLineEdit:focus {{
                border: 2px solid {Theme.PRIMARY};
            }}
            QPushButton {{
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
            }}
            QComboBox {{
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 8px;
                padding: 6px 12px;
                color: {Theme.TEXT_PRIMARY};
            }}
            QComboBox:drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 2px solid {Theme.TEXT_SECONDARY};
                border-bottom: 2px solid {Theme.TEXT_SECONDARY};
                width: 8px;
                height: 8px;
                transform: rotate(-45deg);
                margin-right: 10px;
                margin-top: -2px; 
            }}
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.SECONDARY_PRESSED};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QToolTip {{
                background-color: {Theme.SURFACE};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
                padding: 4px;
            }}
            QMenuBar {{
                background-color: {Theme.BACKGROUND};
                color: {Theme.TEXT_PRIMARY};
            }}
            QMenuBar::item {{
                background-color: transparent;
            }}
            QMenuBar::item:selected {{
                background-color: {Theme.SECONDARY_HOVER};
            }}
            QMenu {{
                background-color: {Theme.SURFACE};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
            }}
            QMenu::item {{
                padding: 6px 24px 6px 12px;
            }}
            QMenu::item:selected {{
                background-color: {Theme.SECONDARY_HOVER};
            }}
        """

    @staticmethod
    def button_primary():
        return f"""
            QPushButton {{
                background-color: {Theme.PRIMARY};
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {Theme.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Theme.PRIMARY_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {Theme.SECONDARY_PRESSED};
                color: {Theme.TEXT_SECONDARY};
            }}
        """

    @staticmethod
    def button_secondary():
        return f"""
            QPushButton {{
                background-color: {Theme.SECONDARY};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.BORDER};
            }}
            QPushButton:hover {{
                background-color: {Theme.SECONDARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Theme.SECONDARY_PRESSED};
            }}
        """
        
    @staticmethod
    def card_style():
        return f"""
            QFrame#Card {{
                background-color: {Theme.SURFACE};
                border: 1px solid {Theme.BORDER};
                border-radius: 12px;
            }}
        """
