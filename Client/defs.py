from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from regui import *
from logui import *
from ui import *
from util import *
import ctypes  # An included library with Python install.   

import pyautogui

class RegWin(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Registerform()
        self.ui.setupUi(self)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.Cancel.clicked.connect(self.close)
        self.setFixedSize(202, 261)
        self.ui.Register.clicked.connect(self.Reg)
        self.ui.label.setPixmap(QtGui.QPixmap("LOGO.jpg"))
    
    def Reg(self):
        if(self.ui.username.text() != "" and self.ui.password.text()!="" and self.ui.confirmpass.text()!=""):
            if(CheckUnUsr(self.ui.username.text())):
                if(check_email(self.ui.email.text())):
                    if(self.ui.password.text() == self.ui.confirmpass.text()):
                        RegisterUser(self.ui.email.text(),self.ui.username.text(),self.ui.password.text())
                        ctypes.windll.user32.MessageBoxW(0, f"Successfully Registered", "User Register", 64) 
                    else:
                        ctypes.windll.user32.MessageBoxW(0, f"Passwords do not match", "Password Mismatch", 48)        
                else:
                    ctypes.windll.user32.MessageBoxW(0, f"The email '{self.ui.email.text()}' does not exist.", "Invalid Username", 48)    
            else:
                ctypes.windll.user32.MessageBoxW(0, f"The Username '{self.ui.username.text()}' already exists.", "Existing Username", 48)
                
            
        else:
            mp = {
                "Username" : self.ui.username.text(),
                "Password" : self.ui.password.text(),
                "Confirm Password" : self.ui.confirmpass.text()
            }
            print(mp)
            lt = []
            for i in mp:
                if(mp[i] == ""):
                    lt.append(i)
            ctypes.windll.user32.MessageBoxW(0, f'{", ".join(lt)} Fields Are Empty', "Empty Fields", 16)
            
            
import requests
import os
from subprocess import Popen
import threading
class LogWin(QWidget):
    def __init__(self,regfunc):
        super().__init__()
        self.ui = Ui_Loginform()
        self.setFixedSize(179, 258)
        self.ui.setupUi(self)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.login.clicked.connect(self.log)
        self.ui.gauth.clicked.connect(regfunc)
        
        self.ui.logo.setPixmap(QtGui.QPixmap("LOGO.jpg"))
    
    def log(self):
        print("success")  
        if(self.ui.password.text() == "" or self.ui.username.text() == ""):
            ctypes.windll.user32.MessageBoxW(0, f"Empty Fields", 16)
        else:
            r = requests.post(f"{GetConfig()['SERVER']['HOST']}/fetchudata/?key={GetConfig()['SERVER']['KEY']}&uid={self.ui.username.text()}")
            try:
                if(self.ui.password.text() == r.json()["meta"][0][-2]):
                    threading.Thread(target= lambda:os.system(f"cd application & python main.py {self.ui.username.text()}")).start()
                    print("AUTHENTICATED")
                else:
                    ctypes.windll.user32.MessageBoxW(0, f"Password for '{self.ui.username.text()}' is invalid", "Invalid Password", 16)
            except:
                ctypes.windll.user32.MessageBoxW(0, f"Password for '{self.ui.username.text()}' is invalid", "Invalid Password", 16)

                print(r.json())
            
            
        
        
