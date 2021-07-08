# -*- coding: utf-8 -*-

#Insira o IP na classe server thread

from PyQt5 import QtGui, QtWidgets, QtCore
import pandas as pd
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
import datetime


class CustomTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(CustomTableModel, self).__init__()
        self.load_data(data)

    def load_data(self, data):
        self.input_Users = data[0].values
        self.input_Inicio = data[1].values
        self.input_Fim = data[2].values
        self.input_Atividade = data[3].values
        self.input_Tempo=data[4].values

        self.column_count = 5
        self.row_count = len(self.input_Atividade)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            
            return ("Usuario", "Inicio", 'Fim', 'Atividade', 'Tempo')[section]
        else:
            return "{}".format(section)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                raw_user = self.input_Users[row]
                
                return raw_user
            elif column == 1:
                return self.input_Inicio[row]
            elif column==2:
                return self.input_Fim[row]
            elif column==3:
                return self.input_Atividade[row]

            elif column==4:
                return self.input_Tempo[row]

        elif role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor(QtCore.Qt.white)
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight

        return None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, df):
        data=self.read_data(df)
        self.cond=True
        self.df=df
        
        self.ativ=''

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 402)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.labelUser=QtWidgets.QLabel(self.centralwidget)
        self.labelUser.setGeometry(QtCore.QRect(135, 0, 150, 22))
        self.labelUser.setText('Escolha o usuário:')

        self.Ring = QtWidgets.QComboBox(self.centralwidget)
        self.Ring.setGeometry(QtCore.QRect(135, 20, 150, 22))
        self.Ring.setObjectName("Ring")
        self.Ring.addItem('Todos os usuarios')
        for item in list(self.df.Usuario.unique()):
            self.Ring.addItem(item)
        #self.Ring.activated.connect(self.selecionar)


        self.labelAtiv=QtWidgets.QLabel(self.centralwidget)
        self.labelAtiv.setGeometry(QtCore.QRect(290, 0, 150, 22))
        self.labelAtiv.setText('Escolha a atividade:')
        self.Ring1 = QtWidgets.QComboBox(self.centralwidget)
        self.Ring1.setGeometry(QtCore.QRect(290,20, 150,22))
        self.Ring1.setObjectName("Ring1")
        self.Ring1.addItem('Todas as atividades')
        for item in list(self.df.Atividade.unique()):
            self.Ring1.addItem(item)
        #self.Ring1.activated.connect(self.selecionaratividade)


        self.Tabela = QtWidgets.QTableView(self.centralwidget)
        self.Tabela.setGeometry(QtCore.QRect(20, 60, 570, 301))
        self.Tabela.setObjectName("Tabela")
        self.Tabela.modelo=CustomTableModel(data)
        self.Tabela.setModel(self.Tabela.modelo)
        self.horizontal_header = self.Tabela.horizontalHeader()
        self.vertical_header = self.Tabela.verticalHeader()
        self.horizontal_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.horizontal_header.setStretchLastSection(False)



        self.labelanda=QtWidgets.QLabel(self.centralwidget)
        self.labelanda.setGeometry(QtCore.QRect(20, 0, 150, 22))
        self.labelanda.setText('Status da atividade:')
        self.Opcoes = QtWidgets.QComboBox(self.centralwidget)
        self.Opcoes.setGeometry(QtCore.QRect(20,20, 110,22))
        self.Opcoes.setObjectName("Andamento")
        self.Opcoes.addItem('Tudo')
        self.Opcoes.addItem('Em andamento')
        self.Opcoes.addItem('Finalizada')
        #self.Ring1.activated.connect(self.clickme)


        self.Button_search = QtWidgets.QPushButton(self.centralwidget)
        self.Button_search.setGeometry(QtCore.QRect(445, 20, 70, 23))
        self.Button_search.setObjectName("Pesquisa")
        self.Button_search.clicked.connect(self.pesquisa)


        self.labelhoras=QtWidgets.QLabel(self.centralwidget)
        self.labelhoras.setGeometry(QtCore.QRect(20, 362, 480, 23))
        #self.labelhoras.setText('Horas Trabalhadas: '+str(self.ativ))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Users activities"))
        self.Button_search.setText(_translate("MainWindow", "Pesquisar"))

    def read_data(self, df):
        # Read the CSV content
        Usuarios = df["Usuario"]
        Inicio=df.Inicio
        Fim=df.Fim
        Atividade=df.Atividade
        Tempo=df.Tempo

        return Usuarios, Inicio, Fim, Atividade, Tempo
    def mod(self):
        global cond
        df=pd.read_csv('Base.csv')
        
        data = self.read_data(df)
        x = CustomTableModel(data)
        self.model=x
        self.Tabela.setModel(x)
        self.df=df
        return list(df.Usuario.unique())

    def pesquisa(self):
        df=pd.read_csv('Base.csv')
        usuario=str(self.Ring.currentText())
        atividade=str(self.Ring1.currentText())
        andamento=str(self.Opcoes.currentText())

        if usuario=='Todos os usuarios':
            if atividade=='Todas as atividades':
                if andamento=='Tudo':
                    df=df
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                elif andamento=='Em andamento':
                    df=df.loc[df.Fim=='Em andamento']
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                else:
                    df=df.loc[df.Fim!='Em andamento']
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))



            else:
                if andamento=='Tudo':
                    df=df.loc[df.Atividade==atividade]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                elif andamento=='Em andamento':
                    df=df.loc[(df.Fim=='Em andamento')&(df.Atividade==atividade)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                else:
                    df=df.loc[(df.Fim!='Em andamento')&(df.Atividade==atividade)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))


        else:
            if atividade=='Todas as atividades':
                if andamento=='Tudo':
                    df=df.loc[df.Usuario==usuario]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                elif andamento=='Em andamento':
                    df=df.loc[(df.Fim=='Em andamento')&(df.Usuario==usuario)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))

                else:
                    df=df.loc[(df.Fim!='Em andamento')&(df.Usuario==usuario)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))


            else:
                if andamento=='Tudo':
                    df=df.loc[(df.Atividade==atividade)&(df.Usuario==usuario)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                elif andamento=='Em andamento':
                    df=df.loc[(df.Fim=='Em andamento')&(df.Atividade==atividade)&(df.Usuario==usuario)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))
                else:
                    df=df.loc[(df.Fim!='Em andamento')&(df.Atividade==atividade)&(df.Usuario==usuario)]
                    new=self.read_data(df)
                    self.Tabela.setModel(CustomTableModel(new))

        if atividade=='Todas as atividades':
            self.ativ='Selecione uma atividade'
        else:
            if usuario=='Todos os usuarios':
                #self.ativ=df.loc[(df.Atividade==atividade)&(df.Fim!='Em andamento'), 'Tempo']
                auxiliar=pd.to_timedelta(df.loc[(df.Atividade==atividade)&(df.Fim!='Em andamento'), 'Tempo'])
                #print(auxiliar)
                s=pd.to_timedelta('0')
                for i in auxiliar:
                    s+=i
                self.ativ=s

                #print(self.ativ)
                #print(type(self.ativ))
                if self.ativ=='0':
                    self.ativ='Em andamento'
                self.labelhoras.setText('Horas Trabalhadas: '+str(self.ativ)+'. Para mais detalhes, escolha um usuário')
            else:
                #self.ativ=df.loc[(df.Atividade==atividade)&(df.Fim!='Em andamento'), 'Tempo']
                auxiliar=pd.to_timedelta(df.loc[(df.Atividade==atividade)&(df.Fim!='Em andamento')&(df.Usuario==usuario), 'Tempo'])
                #print(auxiliar)
                s=pd.to_timedelta('0')
                for i in auxiliar:
                    s+=i
                self.ativ=s

                #print(self.ativ)
                #print(type(self.ativ))
                if self.ativ=='0':
                    self.ativ='Em andamento'
                self.labelhoras.setText('Horas Trabalhadas de '+str(usuario)+' na tarefa '+str(atividade)+': '+str(self.ativ))


            


class ServerThread(Thread):
    def __init__(self,window): 
        Thread.__init__(self) 
        self.window=window

    def run(self): 
        #Insira o Ip do Host em TCP_IP
        TCP_IP = '25.64.19.191' 
        TCP_PORT = 80 
        BUFFER_SIZE = 20  
        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        tcpServer.bind((TCP_IP, TCP_PORT)) 
        threads = []
        tcpServer.listen(4) 

        while True:
            print("Multithreaded Python server : Waiting for connections from TCP clients...") 
            global conn
            (conn, (ip,port)) = tcpServer.accept() 
            newthread = ClientThread(ip,port,self.window) 
            newthread.start() 
            threads.append(newthread) 
        
        for t in threads: 
            t.join() 

class ClientThread(Thread): 
 
    def __init__(self,ip,port,window): 
        Thread.__init__(self) 
        self.window=window
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port)) 
 
    def run(self): 
        while True : 
            
            #(conn, (self.ip,self.port)) = serverThread.tcpServer.accept() 
            global conn
            data = conn.recv(2048) 
            global dictio
            dictio=eval(data)
            #print(data)
            print(dictio)
            self.update_data()
            #print(self.window.Tabela.modelo)
            n=self.window.mod()
            #print(widget.model)
            #self.window.Tabela.setModel(self.window.Tabela.modelo)
           
            
    def update_data(self):
        base=pd.read_csv('Base.csv')
        new_information=pd.DataFrame(dictio)
        new_information.Tempo=datetime.datetime.now()-datetime.datetime.now()
        atividade_new=new_information.Atividade
        nome_new=((new_information.Usuario))
        atividade_new=str(atividade_new[0])
        #print(type(nome_new))
        #print(nome_new)
        #print(nome_new[0])
        nome_new=str(nome_new[0])
        if not(nome_new in list(base.Usuario.unique())):
            self.window.Ring.addItem(nome_new)
        if not(atividade_new in list(base.Atividade.unique())):
            self.window.Ring1.addItem(atividade_new)
        if not(base.empty):
            if nome_new in list(base.Usuario.unique()):
                x=(datetime.datetime.now()-datetime.datetime.strptime(base.loc[((base.Usuario)==nome_new)&(base.Fim=='Em andamento'), 'Inicio'].item().split('.')[0], '%Y-%m-%d %H:%M:%S'))
                base.loc[((base.Usuario)==nome_new)&(base.Fim=='Em andamento'), 'Tempo']=x
                base.loc[(base.Usuario!=nome_new)&(base.Fim=='Em andamento'), 'Tempo']=datetime.datetime.now()-pd.to_datetime(base.loc[(base.Usuario!=nome_new)&(base.Fim=='Em andamento'), 'Inicio'])
            else:
                base.loc[(base.Usuario!=nome_new)&(base.Fim=='Em andamento'), 'Tempo']=datetime.datetime.now()-pd.to_datetime(base.loc[(base.Usuario!=nome_new)&(base.Fim=='Em andamento'), 'Inicio'])
                    
        (base.loc[((base.Usuario)==nome_new)&(base.Fim=='Em andamento'), 'Fim'])=datetime.datetime.now()
        base=base.append(new_information, ignore_index=True)
        base.to_csv('Base.csv', index=False)    



if __name__ == "__main__":

    import sys
    data=pd.read_csv('Base.csv')
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, data)

    serverThread=ServerThread(ui)

    serverThread.start()

    MainWindow.show()
    sys.exit(app.exec_())
    
