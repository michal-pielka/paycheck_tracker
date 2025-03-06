import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui import PaycheckTracker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = PaycheckTracker("config.ini")

    tracker.show()
    sys.exit(app.exec())
