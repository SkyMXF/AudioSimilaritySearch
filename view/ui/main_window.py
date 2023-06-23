# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1009, 348)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditInputFile = QLineEdit(self.groupBox)
        self.lineEditInputFile.setObjectName(u"lineEditInputFile")

        self.horizontalLayout_2.addWidget(self.lineEditInputFile)

        self.pushButtonBrowseInput = QPushButton(self.groupBox)
        self.pushButtonBrowseInput.setObjectName(u"pushButtonBrowseInput")

        self.horizontalLayout_2.addWidget(self.pushButtonBrowseInput)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.label_2)

        self.lineEditInputChannel = QLineEdit(self.groupBox)
        self.lineEditInputChannel.setObjectName(u"lineEditInputChannel")
        self.lineEditInputChannel.setMinimumSize(QSize(150, 0))
        self.lineEditInputChannel.setMaximumSize(QSize(150, 16777215))
        self.lineEditInputChannel.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.lineEditInputChannel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.label_3)

        self.lineEditInputSampleRate = QLineEdit(self.groupBox)
        self.lineEditInputSampleRate.setObjectName(u"lineEditInputSampleRate")
        self.lineEditInputSampleRate.setMinimumSize(QSize(150, 0))
        self.lineEditInputSampleRate.setMaximumSize(QSize(150, 16777215))
        self.lineEditInputSampleRate.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.lineEditInputSampleRate)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.label_4)

        self.lineEditInputDuration = QLineEdit(self.groupBox)
        self.lineEditInputDuration.setObjectName(u"lineEditInputDuration")
        self.lineEditInputDuration.setMinimumSize(QSize(150, 0))
        self.lineEditInputDuration.setMaximumSize(QSize(150, 16777215))
        self.lineEditInputDuration.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.lineEditInputDuration)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditSearchingPath = QLineEdit(self.groupBox_2)
        self.lineEditSearchingPath.setObjectName(u"lineEditSearchingPath")

        self.horizontalLayout_3.addWidget(self.lineEditSearchingPath)

        self.pushButtonBrowseSearching = QPushButton(self.groupBox_2)
        self.pushButtonBrowseSearching.setObjectName(u"pushButtonBrowseSearching")

        self.horizontalLayout_3.addWidget(self.pushButtonBrowseSearching)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_7.addWidget(self.label_5)

        self.lineEditSearchWavNum = QLineEdit(self.groupBox_2)
        self.lineEditSearchWavNum.setObjectName(u"lineEditSearchWavNum")
        self.lineEditSearchWavNum.setMinimumSize(QSize(200, 0))
        self.lineEditSearchWavNum.setMaximumSize(QSize(200, 16777215))
        self.lineEditSearchWavNum.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.lineEditSearchWavNum)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.progressBar = QProgressBar(self.groupBox_3)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonRun = QPushButton(self.groupBox_3)
        self.pushButtonRun.setObjectName(u"pushButtonRun")
        self.pushButtonRun.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_4.addWidget(self.pushButtonRun)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditOutputFolder = QLineEdit(self.groupBox_3)
        self.lineEditOutputFolder.setObjectName(u"lineEditOutputFolder")
        self.lineEditOutputFolder.setReadOnly(True)

        self.horizontalLayout.addWidget(self.lineEditOutputFolder)

        self.pushButtonOpenOutput = QPushButton(self.groupBox_3)
        self.pushButtonOpenOutput.setObjectName(u"pushButtonOpenOutput")
        self.pushButtonOpenOutput.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.pushButtonOpenOutput)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FFAudioMatcher", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Input File (Audio or Video)", None))
        self.pushButtonBrowseInput.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Channels", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Sample Rate", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Duration(s)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Searching Path (Folder)", None))
        self.pushButtonBrowseSearching.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Wav(s) Num", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Run Searching", None))
        self.pushButtonRun.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Output Folder", None))
        self.pushButtonOpenOutput.setText(QCoreApplication.translate("MainWindow", u"Open", None))
    # retranslateUi

