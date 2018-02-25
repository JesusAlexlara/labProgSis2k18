import sys
from aplicacion import MainWindow
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())