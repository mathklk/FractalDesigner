from PyQt5.QtWidgets import *
import drawarea


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self._setupWidgets()

    def _setupWidgets(self):
        self.centralWidget = QWidget()
        self.centralLayout = QGridLayout()
        self.centralWidget.setLayout(self.centralLayout)

        self.button = drawarea.DrawArea()
        self.centralLayout.addWidget(self.button)


        self.setCentralWidget(self.centralWidget)

