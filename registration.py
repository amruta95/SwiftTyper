import sys
import time

from PyQt4 import QtGui, QtCore,uic
from PyQt4 import QtGui, QtCore
from time import strftime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from random import randrange
import sqlite3
import Swift_Typer_Registration,Swift_Typer

conn = sqlite3.connect('swifttyper.db')
form_class = uic.loadUiType("Swift_Typer_Registration.ui")[0]

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

green = 0
red = 0
j = 0

class Registration(QtGui.QMainWindow,form_class):
    para = ""
    randompara = randrange(15)
    value = 0
    words = 0
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def Time(self):
        self.value += 1
        if (self.value%60)<10:
            self.ui.lcdtimer.display(str(self.value/60)+":0"+str(self.value%60))
        else:
            self.ui.lcdtimer.display(str(self.value/60)+":"+str(self.value%60))

    def initUI(self):
        self.Form=QtGui.QMainWindow()
        self.ui=Swift_Typer_Registration.Ui_MainWindow()
        self.ui.setupUi(self.Form)
        self.Form.showFullScreen()
        
        player = self.ui.name1.text()
        regid = self.ui.rno.text()
        colg = self.ui.colg.text()
        phone = self.ui.mob.text()
        wpm = 0
        with conn:
            cur = conn.cursor()
            #cur.execute("insert into registration (regid,name,institute,contact,wpm) values ("+str(regid)+","+player+","+colg+","+str(phone)+","+str(wpm)+")")
            cur.execute("insert into registration (regid,name,institute,contact,wpm) values(?,?,?,?,?)",(str(regid),str(player),str(colg),str(phone),str(wpm)))
            conn.commit()
        self.ui.loginbutton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        print "Registered Successfully"
        form_class = uic.loadUiType("Swift_Typer.ui")[0]
        self.Form2=QtGui.QMainWindow()
        self.ui=Swift_Typer.Ui_MainWindow()
        self.ui.setupUi(self.Form2)
        self.Form2.showFullScreen()

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        with conn:
            cur = conn.cursor()
            cur.execute("select para from paragraphs where id="+str(self.randompara))
            conn.commit()
            row = cur.fetchone()
            print row[0]
            self.para = str(row[0])
        self.ui.textBrowser.append(self.para)
        print 'pakka idhar hi jhol hai'
        print self.ui.lineEdit.textChanged[str]
        self.ui.lineEdit.textChanged[str].connect(self.onChanged)


    def onChanged(self,text):
        global green
        global red
        global j
        currentWord = QString(text)
        str_length = currentWord.length()
        hardCodedPara = QString(self.para)
        for i in range(0,str_length):

            if (j < hardCodedPara.length()):
                if (currentWord[i] == hardCodedPara[j+i]):
                    green+=1           #a counter for the number of correct letters typed
                    tempfloat=100*(green-red)/green
                    self.ui.lcd.display(int(tempfloat))
                    self.Form.setStyleSheet(_fromUtf8("background-color: green;"))     #green
                    if ((j+i+1)<len(hardCodedPara)):
                        if (hardCodedPara[j+i]==' '):
                            j = j + i +1
                            print j
                            self.words+=1
                            if j>hardCodedPara.length():
                                j-=1
                            #j = j + 1
                            self.ui.lineEdit.setMaxLength(0)   #To display only the current word in the textfield
                            #self.lineEdit.text('')
                            print'space'
                    if (j+i+1)==len(hardCodedPara):
                        self.words+=1
                        print "Exit"
                        self.ui.lineEdit.setMaxLength(0)
                        return
                    self.ui.lcdspeed.display(60*self.words/self.value)

                else:
                    #str_length+=1           #to allow the user to backspace and at the same time add the correct letter
                    self.ui.lineEdit.setMaxLength(str_length)      
                    red+=1            #a counter for the number of wrong letters typed
                    tempfloat=100*(green-red)/green
                    self.ui.lcd.display(int(tempfloat))
                    self.Form.setStyleSheet(_fromUtf8("background-color: rgb(200, 10, 10);"))    #red
                    continue    #Repeat the above steps untill the error is resolved
                self.ui.lineEdit.setMaxLength(60)     #Though the textfield will be set to null as and when a space is encountered
                            #Still setting it to 60 so that if the else statements are executed then the textfield should accept the entire word even if the next word is of greater length than the current word
                print "j = ",j
                print "i = ",i
                #j = j + 1
            else:#(hardCodedPara.length()+1):
                #j-=1
                print "Exit"
                self.ui.lineEdit.setMaxLength(0)
                break



if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    registration = Registration()
    sys.exit(app.exec_())
