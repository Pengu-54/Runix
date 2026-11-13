# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'runix_librarynvNgan.ui'
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
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
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
        self.header_lineedit = QLineEdit(self.centralwidget)
        self.header_lineedit.setObjectName(u"header_lineedit")

        self.verticalLayout.addWidget(self.header_lineedit)

        self.flag_lineedit = QLineEdit(self.centralwidget)
        self.flag_lineedit.setObjectName(u"flag_lineedit")

        self.verticalLayout.addWidget(self.flag_lineedit)

        self.edit_json_button = QPushButton(self.centralwidget)
        self.edit_json_button.setObjectName(u"edit_json_button")

        self.verticalLayout.addWidget(self.edit_json_button)

        self.fpic_checkbox = QCheckBox(self.centralwidget)
        self.fpic_checkbox.setObjectName(u"fpic_checkbox")

        self.verticalLayout.addWidget(self.fpic_checkbox)

        self.fpic_label = QLabel(self.centralwidget)
        self.fpic_label.setObjectName(u"fpic_label")

        self.verticalLayout.addWidget(self.fpic_label)

        self.file_ext_lineedit = QLineEdit(self.centralwidget)
        self.file_ext_lineedit.setObjectName(u"file_ext_lineedit")

        self.verticalLayout.addWidget(self.file_ext_lineedit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.savebutton = QPushButton(self.centralwidget)
        self.savebutton.setObjectName(u"savebutton")

        self.verticalLayout.addWidget(self.savebutton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.header_lineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Header name #example #include <QApplication>", None))
        self.flag_lineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Flag", None))
        self.edit_json_button.setText(QCoreApplication.translate("MainWindow", u"Edit Json", None))
        self.fpic_checkbox.setText(QCoreApplication.translate("MainWindow", u"-fPIC", None))
        self.fpic_label.setText(QCoreApplication.translate("MainWindow", u"Optional: If no file extension is specified, `.c` and `.cpp` files will be targeted by default.", None))
        self.file_ext_lineedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"File extension ", None))
        self.savebutton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

