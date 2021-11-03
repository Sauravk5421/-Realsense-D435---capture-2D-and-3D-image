from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 860)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #camera view size
        self.label_show = QtWidgets.QLabel(self.centralwidget)
        self.label_show.setGeometry(QtCore.QRect(10, 0, 1280, 720))
        self.label_show.setObjectName("label_show")
        #Take Normal Photo
        self.Button_colorphoto = QtWidgets.QPushButton(self.centralwidget)
        self.Button_colorphoto.setGeometry(QtCore.QRect(630, 750, 101, 41))
        self.Button_colorphoto.setObjectName("Button_photo")


        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Realsense Window"))
        self.Button_colorphoto.setText(_translate("MainWindow", "Take Pictures"))



