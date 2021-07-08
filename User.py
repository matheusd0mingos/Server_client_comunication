# -*- coding: utf-8 -*-


import sys
import datetime
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 230)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 40, 371, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 100, 371, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 61, 16))
        self.label_2.setObjectName("label_2")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(30, 140, 150, 23))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clickme)
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.sair)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.firstTime=True
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.client=None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Usuário"))
        self.label_2.setText(_translate("MainWindow", "Atividade"))
        self.pushButton.setText(_translate("MainWindow", "Enviar"))
        self.pushButton_2.setText(_translate("MainWindow", "Sair"))

    def clickme(self):
        self.firstTime=False
        name=self.textEdit.toPlainText()
        ativ=self.textEdit_2.toPlainText()
        r = ' "Usuario":' + '["'+ str(name)+'"]' + ', "Inicio":'+ '["'+str(datetime.datetime.now())+'"]'+ ', "Fim": ["Em andamento"]'+', "Atividade":' + '["'+str(ativ)+'"]'
        r='{'+r+'}'
        print('Test1')
        self.client.send(r.encode())
        print('oi')
    
    def sair(self):
        if self.firstTime==True:
            print('oi')
            exit()
        else:
            
            self.client.close() 


class ClientThread(Thread):
    def __init__(self,window): 
        Thread.__init__(self) 
        self.window=window
 
    def run(self): 
       #Insira o ip do host em host
       host = '25.67.200.18' 
       port = 80
       BUFFER_SIZE = 2000 
       self.window.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
       self.window.client.connect((host, port))
       
       #while True:
           #data = tcpClientA.recv(BUFFER_SIZE)
           #self.window.chat.append(data.decode("utf-8"))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    clientThread=ClientThread(ui)
    clientThread.start()
    MainWindow.show()
    sys.exit(app.exec_())
