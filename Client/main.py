
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_Xpense
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import defs





class Landing(QtWidgets.QMainWindow):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui = Ui_Xpense()
        self.ui.setupUi(self)
        self.RegisterWindow = defs.RegWin()
        self.setFixedSize(self.size())
        self.ui.register_2.clicked.connect(self.displayRegWin)
        self.ui.login.clicked.connect(self.displayLogWin)
        self.ui.logo.setPixmap(QtGui.QPixmap("LOGO.jpg"))
    
    def displayRegWin(self):
        self.rw = defs.RegWin()
        self.rw.show()

    def displayLogWin(self):
        self.lw = defs.LogWin(self.displayRegWin)
        self.lw.show()
        

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = Landing()
	ui.show()
	sys.exit(app.exec_())
