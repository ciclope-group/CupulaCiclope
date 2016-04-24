import sys
from Aplicacion2 import *
import serial


class MiFormulario(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        

    def ejemplo():
        print "Holis"

if __name__== "__main__":
    app=QtGui.QApplication(sys.argv)
    myapp = MiFormulario()
    myapp.show()
    sys.exit(app.exec_())
