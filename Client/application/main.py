
from PyQt5 import QtCore, QtGui, QtWidgets
from ui2 import Ui_MainMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import datetime
import threading
import logging
import time
import tkinter as tk
from tkinter import messagebox

import json
import easygui
import requests
from util import *
import configparser
from prodq import *
import ctypes

class CalendarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.calendar = QCalendarWidget(self)
        self.setWindowTitle('Calendar')
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.showDate)
        self.label = QLabel(self)
        self.label.setText(self.calendar.selectedDate().toString())

        layout = QVBoxLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(self.label)

    def showDate(self, date):
        self.label.setText(date.toString())

class Communicate(QObject):
    qd = pyqtSignal()



class MMWindow(QtWidgets.QMainWindow):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.user = sys.argv[1]
        print(GetConfig()["SERVER"]["HOST"])
        self.ui = Ui_MainMainWindow()
        self.expenditure = 0
        self.comms = Communicate()
        self.ui.setupUi(self)
        self.setFixedSize(self.size());

        ct = datetime.datetime.now()
        today = datetime.date.today()
        self.ui.YearProgress.setValue(int(((ct.day+((ct.month-1)*30.5))/365)*100))
        self.ui.MonthProgress.setValue(int((ct.day/30.5)*100))
        curr = ['₹',"$",'₵', 'ƒ', 'Fr', 'gr', 'kr', 'ps', '£',"₿"]
        for i in curr:
            self.ui.currencies.addItem(i)

        self.ui.Totalexpend_4.setStyleSheet("text-align:center;")
        self.ui.Totalexpend_5.setStyleSheet("text-align:center;")
        self.ui.Totalexpend_5.setText(f"{today}")
        self.ui.pushButton.clicked.connect(lambda: threading.Thread(target=self.search_products).start())
        
        #self.central_widget = QWidget()

        # Add a widget to the scroll area
        self.scroll_widget = QWidget()
        self.scroll_widget.setGeometry(0, 0, 780, 2000)
        self.scroll_widget_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_widget_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_widget1 = QWidget()
        self.scroll_widget1.setGeometry(0, 0, 780, 2000)
        self.scroll_widget1_layout = QVBoxLayout(self.scroll_widget1)
        self.scroll_widget1_layout.setAlignment(Qt.AlignTop)

        self.scroll_widget2 = QWidget()
        self.scroll_widget2.setGeometry(0, 0, 780, 2000)
        self.scroll_widget2_layout = QVBoxLayout(self.scroll_widget2)
        self.scroll_widget2_layout.setAlignment(Qt.AlignTop)

        # Set the scroll area's widget
        self.ui.orderscrolla.setWidget(self.scroll_widget)
        self.ui.recently.setWidget(self.scroll_widget1)
        self.ui.search.setWidget(self.scroll_widget2)

        # Add a button to open the dialog box

        self.ui.Add.clicked.connect(lambda : self.show_dialog_box(1))
        self.ui.Add_2.clicked.connect(lambda : self.show_dialog_box(2))
        self.ui.clear.clicked.connect(lambda:self.clear_session())
        self.ui.calendar.clicked.connect(lambda: self.showCalendar())
        self.ui.calendar_2.clicked.connect(lambda: self.showcurrconv())
        self.comms.qd.connect(self.add_searched_products)
        # Initialize the list of items
        self.orders_item_list = []
        self.recently_item_list = []
        self.search_widgets = []

        self.setup_udata(self.user)
    
    def showcurrconv(self):
        curr_codes = ['USD','INR','AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL', 'BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'DOT', 'AVAX', 'MATIC', 'LTC', 'ADA']
        Dialog = QDialog(self)
        
        Dialog.setWindowTitle("Convert Currency")
        Dialog.setObjectName("Currency Converter")
        Dialog.resize(354, 185)
        Dialog.setFixedSize(Dialog.size())
        convert = QtWidgets.QPushButton(Dialog)
        convert.setGeometry(QtCore.QRect(140, 140, 75, 23))
        convert.setObjectName("convert")
        convert.setText("Convert")
        inp_value = QtWidgets.QLineEdit(Dialog)
        inp_value.setGeometry(QtCore.QRect(50, 60, 81, 41))
        inp_value.setObjectName("inp_value")
        out_val = QtWidgets.QTextBrowser(Dialog)
        out_val.setGeometry(QtCore.QRect(220, 60, 81, 41))
        out_val.setObjectName("out_val")
        out_val.setStyleSheet("text-align:center;")
        inp_curr = QtWidgets.QComboBox(Dialog)
        inp_curr.setGeometry(QtCore.QRect(50, 30, 81, 22))
        inp_value.setAlignment(QtCore.Qt.AlignCenter)
        inp_curr.setObjectName("inp_curr")
        out_curr = QtWidgets.QComboBox(Dialog)
        out_curr.setGeometry(QtCore.QRect(220, 30, 81, 22))
        out_curr.setObjectName("out_curr")
        label = QtWidgets.QLabel(Dialog)
        label.setGeometry(QtCore.QRect(140, 40, 71, 81))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        label.setFont(font)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setObjectName("label")
        label.setText("TO")

        for i in curr_codes:
            inp_curr.addItem(i)
            out_curr.addItem(i)
        convert.clicked.connect(lambda:self.convert_currency(inp_value.text() , out_val ,inp_curr.currentText() , out_curr.currentText()))

        Dialog.exec_()

    def convert_currency(self, input_value, output_label,input_curr,output_curr):
        # For example, you could use an API like Fixer.io or OpenExchangeRates.org
        # to get the latest exchange rates and perform the conversion.
        # For the purpose of this example, we'll just assume a fixed conversion rate of 1 USD = 0.85 EUR
        try:
            otpt = ""
            for i in input_value:
                if(i.isdigit()):
                    otpt+=i
            input_value = float(otpt)
        except:
            pass
        print(input_curr,output_curr)
        h = f"{GetConfig()['SERVER']['HOST']}/convert/?key={GetConfig()['SERVER']['KEY']}&currin={output_curr.lower()}&currout={input_curr.lower()}"
        print(h)
        r = requests.get(h)
        print(r.json())
        if(otpt == ""):
            pass
        else:
            output_label.setText(str(r.json()['data'][output_curr]['value']*input_value))
    
    def showCalendar(self):
        self.calendar_window = CalendarWindow()
        self.calendar_window.show()

    def setup_udata(self,uid):
        r = requests.post(f"{GetConfig()['SERVER']['HOST']}/fetchudata/?key={GetConfig()['SERVER']['KEY']}&uid={uid}").json()
        print(r)
        self.ui.Totalexpend_4.setText(f"{r['udata']['expenditure']}")
        self.expenditure = float(r['udata']['expenditure'])
        for i in r["udata"]["orders"]:
            if(i == "placeholder"):
                break
            self.save_item(i["name"],i["price"],i["link"],None,1,i["image"])
        for i in r["udata"]["recently_bought"]:
            if(i == "placeholder"):
                break
            self.save_item(i["name"],i["price"],i["link"],None,2,i["image"])
        
    def show_dialog_box(self,arg):
        dialog = QDialog()
        dialog.setWindowTitle("Add Item")
        dialog.setModal(True)
        dialog_layout = QVBoxLayout()

        # Add input fields to the dialog box
        name_label = QLabel("Item Name:")
        name_input = QLineEdit()
        dialog_layout.addWidget(name_label)
        dialog_layout.addWidget(name_input)

        price_label = QLabel("Item Price:")
        price_input = QLineEdit()
        dialog_layout.addWidget(price_label)
        dialog_layout.addWidget(price_input)

        link_label = QLabel("Item Link:(MUST BE Amazon(IN)/Flipkart Product URL)")
        link_input = QLineEdit()
        dialog_layout.addWidget(link_label)
        dialog_layout.addWidget(link_input)

        
        save_button = QPushButton("Save", dialog)
        save_button.clicked.connect(lambda: self.save_item(name_input.text(), price_input.text(), link_input.text(), dialog,arg))
        dialog_layout.addWidget(save_button)
        
        self.status_label = QLabel("")
        dialog_layout.addWidget(self.status_label)
        # Set the layout and show the dialog box
        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def float_check(self,s):
        try:
            float(s)
            return True
        except:
            return False

    def save_item(self, name, price, link, dialog,box,img=None):

        if(name == ""):
            ctypes.windll.user32.MessageBoxW(0, f"Empty Name Field", "Invalid Name", 16)
            return
        if(self.float_check(price)):
            try:
                self.status_label.setText("Saving........")
            except:
                pass
            if(img):
                image_url = img
            else:            
                if("dp" in link.split("/")):
                    asin  = link.split("/")[link.split("/").index("dp")+1]
                    print("FAIJAFPOUAHFUAOUFAJIOJFA")
                    image_url = AmazonQuery.GetProductInfo(asin)["img"]
                    print("POUAHFUAOUFAJIOJFA")
                    
                else:
                    #ctypes.windll.user32.MessageBoxW(0, f"Link must be a valid Amazon(IN)/Flipkart URL", "Invalid Link", 16)
                    root = tk.Tk()
                    root.withdraw()
                    result = messagebox.askquestion("Invalid Link", "Link must be a valid Amazon(IN)/Flipkart URL\nAre You Sure You Want To Proceed?", icon="warning")
                    if result == 'yes':
                        image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxtBQ_FQ2Ks84HAs5WOFXBPVVsU9ncT1IFPg"
                    else:
                        try:
                            self.status_label.setText("")
                        except:
                            pass
                        return
        

            # Add the item to the list and create a widget to display it
            item = {"name": name, "price": price, "link": link, "image": image_url}
            imap = [self.orders_item_list,self.recently_item_list]
            imap[box-1].append(item)
            item_widget = self.create_item_widget(item,box)
            if(box==1 or box==2):
                self.expenditure+=float(item['price'])
                self.ui.Totalexpend_4.setText(str(self.expenditure))


            # Add the widget to the scrollable area and close the dialog box
            lmap = [self.scroll_widget_layout , self.scroll_widget1_layout]
            lmap[box-1].addWidget(item_widget)
            try:
                dialog.close()
            except:
                pass
            try:
                self.status_label.setText("")
            except:
                pass
            self.sync_udata(self.user)
        else:
            try:
                float(price)        
            except:
                ctypes.windll.user32.MessageBoxW(0, f"Price must a float", "Invalid Price", 16)
                return False

            # if(not("dp" in link.split("/"))):
            #     ctypes.windll.user32.MessageBoxW(0, f"Link must be a valid Amazon(IN)/Flipkart URL", "Invalid Link", 16)

    def sync_udata(self,uid):
        r = requests.post(f"{GetConfig()['SERVER']['HOST']}/fetchudata/?key={GetConfig()['SERVER']['KEY']}&uid={uid}").json()
        r['udata']['orders'] =  self.orders_item_list
        r['udata']['recently_bought'] = self.recently_item_list
        r['udata']['expenditure'] = self.expenditure

        requests.post(f"{GetConfig()['SERVER']['HOST']}/alterudata/?key=123&uid=1",json=r["udata"])

    def clear_session(self):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askquestion("Clear Session Data", "Are You Sure You Want To Clear All Session Data\n(All Data Will Be UNRETRIEVABLE)\nXpense Will Automatically Close and Reset.\nReopen Xpense after clicking Yes.", icon="warning")
        if result == 'yes':
            self.orders_item_list = []
            self.recently_item_list = []
            self.expenditure = 0
            self.sync_udata(self.user)
            exit()
        else:
            pass

    def create_item_widget(self, item,box):
        # Create a widget to display the item
        widget = QWidget()
        widget.setFixedSize(321, 92)
        widget.item_data = item
        horizontalLayout = QtWidgets.QHBoxLayout(widget)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setObjectName("horizontalLayout")
        ProdInfo = QtWidgets.QTextBrowser(widget)
        ProdInfo.setOpenExternalLinks(True)
        ProdInfo.setReadOnly(True)
        ProdInfo.setStyleSheet("color: rgb(0,0,0);\n"
"background-color: rgb(255,255,255);\n"
"font: 8pt \"Leelawadee\"\n"
"")
        ProdInfo.setObjectName("ProdInfo")
        ProdInfo.setText(f"""
Item Name : {item['name']}
Item Price : {item['price']}
        """)
        link = item["link"]
        ProdInfo.append(f"<a href='{link}'>Item URL</a>")
        ProdInfo.resize(186,71)
        horizontalLayout.addWidget(ProdInfo)
        ProdImage = QtWidgets.QLabel(widget)
        ProdImage.resize(47,71)
        ProdImage.setAlignment(QtCore.Qt.AlignCenter)
        ProdImage.setObjectName("ProdImage")
        
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(requests.get(item["image"]).content)
        ProdImage.setPixmap(pixmap.scaled(ProdImage.width(), ProdImage.height(),Qt.KeepAspectRatio))
        horizontalLayout.addWidget(ProdImage)
        
        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")
        if(box!=3):
            cancel = QtWidgets.QPushButton(widget)
            cancel.clicked.connect(lambda:self.remove_item(widget,box))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(cancel.sizePolicy().hasHeightForWidth())
            cancel.setSizePolicy(sizePolicy)
            cancel.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("static/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            cancel.setIcon(icon)
            cancel.setObjectName("cancel")
            verticalLayout.addWidget(cancel)
        if(box ==1 or box==3):
            transfer = QtWidgets.QPushButton(widget)
            #
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(transfer.sizePolicy().hasHeightForWidth())
            transfer.setSizePolicy(sizePolicy)
            transfer.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("static/transfer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            transfer.setIcon(icon1)
            transfer.setObjectName("transfer")
            if(box==1):
                transfer.clicked.connect(lambda: self.transfer_item(widget))
            if(box==3):
                transfer.clicked.connect(lambda: self.transfer_search_item(widget))
            verticalLayout.addWidget(transfer)
        horizontalLayout.addLayout(verticalLayout)

        # Add the item's name, price, and link to the widget
        # info_layout = QVBoxLayout()
        # name_label = QLabel(item["name"])
        # price_label = QLabel(item["price"])
        # link_label = QLabel(item["link"])
        # link_label.setReadOnly(True)
        # info_layout.addWidget(name_label)
        # info_layout.addWidget(price_label)
        # info_layout.addWidget(link_label)
        # widget_layout.addLayout(info_layout)

        return widget
    
    def remove_item(self,obj,box):
        #box 1 orders
        #box 2 recent
        if(box == 3):
            obj.hide()
            return
        obj.hide()
        imap = [self.orders_item_list,self.recently_item_list]
        imap[box-1].remove(obj.item_data)
        self.expenditure -= float(obj.item_data["price"])
        self.ui.Totalexpend_4.setText(str(self.expenditure))

        print("Removed : " , obj.item_data)
        print(imap[box-1])
        self.sync_udata(self.user)

    def transfer_item(self,obj):
        data = obj.item_data
        self.remove_item(obj,1)
        #self.expenditure += float(obj.item_data["price"])
        self.ui.Totalexpend_4.setText(str(self.expenditure))
        self.save_item(data['name'],data['price'],data['link'],None,2,data['image'])

    def transfer_search_item(self,obj):
        data = obj.item_data
        otpt = ""
        for i in str(obj.item_data["price"]):
            if(i.isdigit()):
                otpt+=i
        print(obj.item_data["price"],otpt)
        obj.item_data["price"] = otpt
        self.save_item(data['name'],data['price'],data['link'],None,1,data['image'])

    def search_products(self):
        print("Searching......")
        self.ui.status.setText("Searching The Web.......")
        q = self.ui.lineEdit.text()
        for i in self.search_widgets:
            i.hide()
        self.search_widgets = []
        items = []
        for i in AmazonQuery.SearchProducts(q):
            otpt = AmazonQuery.GetProductInfo(i)
            items.append({"name":otpt["title"] , "price":otpt["price"] , "link" : f"https://www.amazon.in/dp/{otpt['ASIN']}" , "image" : otpt["img"] , "stars":otpt["stars"]})
        
        for i in FlipkartQuery.SearchProducts(q):
            items.append({"name" : i["name"] , "price" : i["current_price"] , "link" : i["link"] , "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxtBQ_FQ2Ks84HAs5WOFXBPVVsU9ncT1IFPg", "stars":FlipkartQuery.GetProductRating(i["query_url"])})

        with open('query.json', 'w') as convert_file:
            convert_file.write(json.dumps(items))
        self.comms.qd.emit()
        #item = {"name": name, "price": price, "link": link, "image": image_url}
        # for i in items:
        #     item_widget = self.create_item_widget(i,3)
        #     self.scroll_widget2_layout.addWidget(item_widget)
        
    def add_searched_products(self):
        f = open('query.json')
        items = json.load(f)
        print(items)
        print("JSON DATA READ")
        for i in items:
            item_widget = self.create_item_widget(i,3)
            self.search_widgets.append(item_widget)
            self.scroll_widget2_layout.addWidget(item_widget)
        self.ui.status.setText("")

  



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ui = MMWindow()
	ui.show()
	sys.exit(app.exec_())
 
 