import sys
import os
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtWidgets import *

def resource_path(relative_path):
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

class MyWindow(QDialog,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.srcPath = ""
        self.dstPath = ""
        self.copyFile = ""
        self.sizeFlag = False
        self.progressBar.setValue(0)

        self.initDisplay()
        self.btnSrcDir.clicked.connect(self.selectSrcDir)
        self.btnDstDir.clicked.connect(self.selectDstDir)
        self.btnCopy.clicked.connect(self.copy)

    def initDisplay(self):
        try:
            f = open('File_Transfer_DataBase.txt','r')
            data = {}
            lines = f.readlines()
            for line in lines:
                separateIdx = line.find(":")
                key = line[:separateIdx]
                value = line[separateIdx+1:-1]
                data[key] = value
            f.close()
            print(data)
            self.srcPath = data["srcPath"]
            self.dstPath = data["dstPath"]
            self.copyFile = data["copyFile"]
            if(self.srcPath==""):
                self.txtSrcPathDisplay()
                self.txtCopyFileDisplay()
            else:
                self.txtSrcPathDisplay(self.srcPath)
                self.txtCopyFileDisplay(self.copyFile)
            if(self.dstPath==""):
                self.txtDstPathDisplay()
            else:
                self.txtDstPathDisplay(self.dstPath)
        except:
            pass

    def saveData(self):
        f = open('File_Transfer_DataBase.txt','w')
        data = {"srcPath":self.srcPath, "dstPath":self.dstPath,"copyFile":self.copyFile}
        for i,(key,value) in enumerate(data.items()):
            f.write("".join("{}:{}\n".format(key, value)))
        f.close()

    def selectSrcDir(self):
        try:
            tempSrcPath = QFileDialog.getOpenFileName(self, 'Open File', '','All File(*)')
            srcPathIdx = tempSrcPath[0].rfind('/')
            srcPath = tempSrcPath[0][:srcPathIdx]
            print(srcPath)
            self.copyFile = tempSrcPath[0][srcPathIdx+1:]
            self.srcPath = srcPath
            self.txtSrcPathDisplay(self.srcPath)
            self.txtCopyFileDisplay(self.copyFile)
        except:
            pass
        if self.srcPath =="":
            self.txtSrcPathDisplay()
            self.txtCopyFileDisplay()
        self.saveData()
        self.progressBar.setValue(0)

    def selectDstDir(self):
        try:
            dstPath = QFileDialog.getExistingDirectory(self, "Select Directory")
            print(1)
            self.dstPath = dstPath
            print(dstPath)
            self.txtDstPathDisplay(self.dstPath)
            print(3)
        except:
            pass
        if self.dstPath =="":
            self.txtDstPathDisplay()
        self.saveData()
        self.progressBar.setValue(0)

    def txtSrcPathDisplay(self,srcPath="Src Dir Path Display"):
        self.txtDisplaySrcPath.setText(srcPath)

    def txtDstPathDisplay(self,dstPath="Dst Dir Path Display"):
        self.txtDisplayDstPath.setText(dstPath)

    def txtCopyFileDisplay(self,copyFileName="Copy File Name Display"):
        self.txtDisplayFile.setText(copyFileName) 

    
    def copy(self):
        try:
            self.copyProcess()
            if((self.srcPath=="") or (self.dstPath=="")):
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle('Error Message')
                error_dialog.setText('There\'s Something Wrong')
                error_dialog.exec_()
            else:
                self.animateProgressBar()
        except:
            pass

    def animateProgressBar(self):
        self.progressBar.setValue(0)
        self.animation = QPropertyAnimation(self.progressBar,b"value")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(100)
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.start()

    def copyProcess(self):
        srcCopyPath = self.srcPath.replace('/','\\')
        dstCopyPath = self.dstPath.replace('/','\\')
        copyFileName = self.copyFile
        if (not(os.path.exists(os.path.join(srcCopyPath,copyFileName)))):
            return

        if (os.path.exists(os.path.join(dstCopyPath,copyFileName))):
            os.system('del {0}'.format(os.path.join(dstCopyPath,copyFileName)))
        os.system('copy {0} {1}'.format(os.path.join(srcCopyPath,copyFileName),dstCopyPath))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWindow = MyWindow()
	myWindow.show()
	app.exec_()