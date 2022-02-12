import sys
from PyQt5.QtWidgets import QApplication
import mainwindow

def main():
    app = QApplication(sys.argv)
    myMainwindow = mainwindow.Mainwindow()
    myMainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
