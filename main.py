from UI.main_ui import ChowsMainWindow
from PyQt5 import QtWidgets, QtCore
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ChowsMainWindow()
    MainWindow.show()
    file = open("UI\Medize.qss",'r')
    with file:
        qss = file.read()
        app.setStyleSheet(qss)
    sys.exit(app.exec_())