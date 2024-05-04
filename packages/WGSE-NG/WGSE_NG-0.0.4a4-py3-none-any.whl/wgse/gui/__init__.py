import sys

from PySide6.QtWidgets import QApplication

from wgse.gui.main import WGSEWindow

app = QApplication(sys.argv)
widget = WGSEWindow()
widget.show()
sys.exit(app.exec())