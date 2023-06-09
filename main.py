import sys, melodieMetroid, automode
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import j2l.pytactx.agent as pytactx


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.area = "" # On créer des attributs pour sauvegarder les textes entrés jusqu'à ce que le bouton connect soit cliqué
        self.password = ""
        self.nom = ""
        self.auto = False
        self.agent = None
        # On crée un timer pour régulièrement envoyer les requetes de l'agent au server et actualiser son état 
        self.timer = QtCore.QTimer()
        self.timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.onTimerUpdate)
        self.ui = uic.loadUi("login.ui", self)


        self.imageRight = QPixmap("samusdroite.png")
        self.imageLeft = QPixmap("samusgauche.png")
        self.imageUp = QPixmap("samushaut.png")
        self.imageDown = QPixmap("samusbas.png")
        self.ui.samusagent.setPixmap(self.imageRight)

    def onTextChange(self, nom):
        self.nom = nom
        print("nom change", nom)

    
    def onTextChange2(self, password):
        self.password = password
        print("password change", password)
    
    def onTextChange3(self, area):
        self.area = area
        print("area change", area)
        

    def onButtonClick(self):
        self.timer.start()
        self.agent = pytactx.AgentFr(
        nom=self.nom, 
        arene=self.area, 
        username="demo",
        password=self.password,
        url="mqtt.jusdeliens.com", 
        verbosite=3
        )
        #Passer vers le fichier automode
        automode.agent= self.agent

    def moveUp(self, haut):
        self.haut = haut
        self.agent.deplacer(0,-1)
        self.agent.orienter(1)
        print("direction haut", haut)

    
    def moveDown(self, bas):
        self.bas = bas
        self.agent.deplacer(0,1)
        self.agent.orienter(3)
        print("direction bas", bas)

    def moveLeft(self, gauche):
        self.gauche = gauche
        self.agent.deplacer(-1,0)
        self.agent.orienter(2)
        print("direction gauche", gauche)

    def moveRight(self, droite):
        self.droite = droite
        self.agent.deplacer(1,0)
        self.agent.orienter(0)
        print("direction droite", droite)
    
    def onAutomode(self, auto):
        self.auto = auto
        print("choix auto", auto)
    
    def manualChoice(self, manuel):
        self.manuel = manuel
        print("choix manuel", manuel)
    
    def shootButton(self, tir):
        self.tir = tir
        if self.tir == True:
            self.agent.tirer(True)
        else:
            self.agent.tirer(False)
        print("tirer", tir)

    def onTimerUpdate(self):
        if ( self.agent != None ):
            self.agent.actualiser()
            if self.auto == True:#Quand le boutton auto est checké
                automode.actualiserEtat()
            # MAJ de la ui selon l'état du robot
            if ( self.agent.vie > self.ui.lifebar.maximum() ):
                self.ui.lifebar.setMaximum(self.agent.vie)
            self.ui.lifebar.setValue(self.agent.vie)
            if self.agent.vie == 0:
                self.agent.robot.playMelody(melodieMetroid.ariveePlanete)
            if self.agent.orientation == 1:
                self.ui.samusagent.setPixmap(self.imageUp)
            if self.agent.orientation == 3:
                self.ui.samusagent.setPixmap(self.imageDown)
            if self.agent.orientation == 2:
                self.ui.samusagent.setPixmap(self.imageLeft)
            if self.agent.orientation == 0:
                self.ui.samusagent.setPixmap(self.imageRight)
    
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()