# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'runix_language_uiVROAsp.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.warninlabel = QLabel(self.centralwidget)
        self.warninlabel.setObjectName(u"warninlabel")

        self.verticalLayout.addWidget(self.warninlabel)

        self.execLineEdit = QLineEdit(self.centralwidget)
        self.execLineEdit.setObjectName(u"execLineEdit")

        self.verticalLayout.addWidget(self.execLineEdit)

        self.FileextensionLineedit = QLineEdit(self.centralwidget)
        self.FileextensionLineedit.setObjectName(u"FileextensionLineedit")

        self.verticalLayout.addWidget(self.FileextensionLineedit)

        self.Namelineedit = QLineEdit(self.centralwidget)
        self.Namelineedit.setObjectName(u"Namelineedit")

        self.verticalLayout.addWidget(self.Namelineedit)

        self.inter_radiob = QRadioButton(self.centralwidget)
        self.inter_radiob.setObjectName(u"inter_radiob")

        self.verticalLayout.addWidget(self.inter_radiob)

        self.BB_radiob = QRadioButton(self.centralwidget)
        self.BB_radiob.setObjectName(u"BB_radiob")

        self.verticalLayout.addWidget(self.BB_radiob)

        self.compileradiob = QRadioButton(self.centralwidget)
        self.compileradiob.setObjectName(u"compileradiob")

        self.verticalLayout.addWidget(self.compileradiob)

        self.Cfe_lineedit = QLineEdit(self.centralwidget)
        self.Cfe_lineedit.setObjectName(u"Cfe_lineedit")

        self.verticalLayout.addWidget(self.Cfe_lineedit)

        self.execute_command_lineedit = QLineEdit(self.centralwidget)
        self.execute_command_lineedit.setObjectName(u"execute_command_lineedit")

        self.verticalLayout.addWidget(self.execute_command_lineedit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.applybutton = QPushButton(self.centralwidget)
        self.applybutton.setObjectName(u"applybutton")

        self.verticalLayout.addWidget(self.applybutton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"LanguageWindow", None))
        self.warninlabel.setText(QCoreApplication.translate("MainWindow", u"Use special placeholders only (e.g. rcc=file). Real filenames are not allowed", None))
        self.execLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Exec #Example g++ rcc=file -o rcc=compiledfile", None))
        self.FileextensionLineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"File extension", None))
        self.Namelineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Compiler or Interpreter name", None))
        self.inter_radiob.setText(QCoreApplication.translate("MainWindow", u"Interpreter", None))
        self.BB_radiob.setText(QCoreApplication.translate("MainWindow", u"Binary or Bytecode", None))
        self.compileradiob.setText(QCoreApplication.translate("MainWindow", u"Compile", None))
        self.Cfe_lineedit.setText(QCoreApplication.translate("MainWindow", u"ELF", None))
        self.Cfe_lineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Compiled File Type Extension", None))
        self.execute_command_lineedit.setText(QCoreApplication.translate("MainWindow", u"./ELF", None))
        self.execute_command_lineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Execute command", None))
        self.applybutton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
    # retranslateUi

