# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpinBox,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(678, 1220)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Profiles = QGroupBox(self.centralwidget)
        self.Profiles.setObjectName(u"Profiles")
        self.profileComboBox = QComboBox(self.Profiles)
        self.profileComboBox.setObjectName(u"profileComboBox")
        self.profileComboBox.setGeometry(QRect(120, 40, 401, 61))
        self.widget = QWidget(self.Profiles)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(180, 110, 291, 241))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.newProfileButton = QPushButton(self.widget)
        self.newProfileButton.setObjectName(u"newProfileButton")

        self.verticalLayout_2.addWidget(self.newProfileButton)

        self.copyProfileButton = QPushButton(self.widget)
        self.copyProfileButton.setObjectName(u"copyProfileButton")

        self.verticalLayout_2.addWidget(self.copyProfileButton)

        self.deleteProfileButton = QPushButton(self.widget)
        self.deleteProfileButton.setObjectName(u"deleteProfileButton")

        self.verticalLayout_2.addWidget(self.deleteProfileButton)


        self.verticalLayout.addWidget(self.Profiles)

        self.Configuration = QGroupBox(self.centralwidget)
        self.Configuration.setObjectName(u"Configuration")
        self.saveProfileButton = QPushButton(self.Configuration)
        self.saveProfileButton.setObjectName(u"saveProfileButton")
        self.saveProfileButton.setGeometry(QRect(460, 30, 171, 81))
        self.widget1 = QWidget(self.Configuration)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(40, 30, 241, 371))
        self.verticalLayout_3 = QVBoxLayout(self.widget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget1)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Venomica"])
        font.setPointSize(14)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2)

        self.label_4 = QLabel(self.widget1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.widget1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.label_5)

        self.label_6 = QLabel(self.widget1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout_3.addWidget(self.label_6)

        self.label_7 = QLabel(self.widget1)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.verticalLayout_3.addWidget(self.label_7)

        self.label_9 = QLabel(self.widget1)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.verticalLayout_3.addWidget(self.label_9)

        self.label_8 = QLabel(self.widget1)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.verticalLayout_3.addWidget(self.label_8)

        self.widget2 = QWidget(self.Configuration)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(280, 30, 181, 371))
        self.verticalLayout_4 = QVBoxLayout(self.widget2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.clientIdEdit = QLineEdit(self.widget2)
        self.clientIdEdit.setObjectName(u"clientIdEdit")

        self.verticalLayout_4.addWidget(self.clientIdEdit)

        self.stateEdit = QLineEdit(self.widget2)
        self.stateEdit.setObjectName(u"stateEdit")

        self.verticalLayout_4.addWidget(self.stateEdit)

        self.detailsEdit = QLineEdit(self.widget2)
        self.detailsEdit.setObjectName(u"detailsEdit")

        self.verticalLayout_4.addWidget(self.detailsEdit)

        self.largeImageEdit = QLineEdit(self.widget2)
        self.largeImageEdit.setObjectName(u"largeImageEdit")

        self.verticalLayout_4.addWidget(self.largeImageEdit)

        self.largeTextEdit = QLineEdit(self.widget2)
        self.largeTextEdit.setObjectName(u"largeTextEdit")

        self.verticalLayout_4.addWidget(self.largeTextEdit)

        self.smallImageEdit = QLineEdit(self.widget2)
        self.smallImageEdit.setObjectName(u"smallImageEdit")

        self.verticalLayout_4.addWidget(self.smallImageEdit)

        self.smallTextEdit = QLineEdit(self.widget2)
        self.smallTextEdit.setObjectName(u"smallTextEdit")

        self.verticalLayout_4.addWidget(self.smallTextEdit)

        self.intervalSpinBox = QSpinBox(self.widget2)
        self.intervalSpinBox.setObjectName(u"intervalSpinBox")

        self.verticalLayout_4.addWidget(self.intervalSpinBox)


        self.verticalLayout.addWidget(self.Configuration)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMouseTracking(True)
        self.statusLabel = QLabel(self.groupBox)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setGeometry(QRect(230, 50, 161, 71))
        font1 = QFont()
        font1.setFamilies([u"Venomica"])
        font1.setPointSize(24)
        font1.setBold(False)
        self.statusLabel.setFont(font1)
        self.widget3 = QWidget(self.groupBox)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(50, 140, 551, 161))
        self.horizontalLayout = QHBoxLayout(self.widget3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.startButton = QPushButton(self.widget3)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout.addWidget(self.startButton)

        self.stopButton = QPushButton(self.widget3)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout.addWidget(self.stopButton)

        self.themeButton = QPushButton(self.widget3)
        self.themeButton.setObjectName(u"themeButton")

        self.horizontalLayout.addWidget(self.themeButton)

        self.exitButton = QPushButton(self.widget3)
        self.exitButton.setObjectName(u"exitButton")

        self.horizontalLayout.addWidget(self.exitButton)


        self.verticalLayout.addWidget(self.groupBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 678, 33))
        self.menuPresenceUI = QMenu(self.menubar)
        self.menuPresenceUI.setObjectName(u"menuPresenceUI")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuPresenceUI.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Profiles.setTitle(QCoreApplication.translate("MainWindow", u"Profiles", None))
        self.newProfileButton.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.copyProfileButton.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.deleteProfileButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.Configuration.setTitle(QCoreApplication.translate("MainWindow", u"Configuration", None))
        self.saveProfileButton.setText(QCoreApplication.translate("MainWindow", u"Save Profile", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Client ID:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"State:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Details:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Image Key:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Large Text:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Small Image Key:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Small Text:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Interval:", None))
        self.clientIdEdit.setText("")
        self.stateEdit.setText("")
        self.detailsEdit.setText("")
        self.largeImageEdit.setText("")
        self.largeTextEdit.setText("")
        self.smallImageEdit.setText("")
        self.smallTextEdit.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"\u25b6 Start", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"\u25a0 Stop", None))
        self.themeButton.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"\u2716 Exit", None))
        self.menuPresenceUI.setTitle(QCoreApplication.translate("MainWindow", u"PresenceUI", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

