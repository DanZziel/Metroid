import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import j2l.pytactx.agent as pytactx


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("login.ui", self)

    def onTextChange(self, nom):
        self.nom = nom

    def onTextChange2(self, password):
        self.password = password
        
    def onTextChange3(self, area):
        self.area = area
        

    def onButtonClick(self):
        agent = pytactx.AgentFr(
        nom=self.nom, 
        arene=self.area, 
        username="demo",
        password=self.password,
        url="mqtt.jusdeliens.com", 
        verbosite=3
        )

        while True:
            agent.orienter((agent.orientation+1)%4)
            agent.actualiser()

        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()