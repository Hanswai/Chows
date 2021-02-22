from UI.main_ui import ChowsMainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ChowsMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())