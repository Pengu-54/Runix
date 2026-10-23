# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'runix-settings1DsHnRk.ui'
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
from PyQt6.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_SettingWindow(object):
    def setupUi(self, SettingWindow):
        if not SettingWindow.objectName():
            SettingWindow.setObjectName(u"SettingWindow")
        SettingWindow.resize(800, 600)
        self.centralwidget = QWidget(SettingWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Terminalcombobox = QComboBox(self.tab)
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.addItem("")
        self.Terminalcombobox.setObjectName(u"Terminalcombobox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Terminalcombobox.sizePolicy().hasHeightForWidth())
        self.Terminalcombobox.setSizePolicy(sizePolicy)
        self.Terminalcombobox.setMinimumSize(QSize(0, 35))

        self.verticalLayout_2.addWidget(self.Terminalcombobox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.applybutton = QPushButton(self.tab)
        self.applybutton.setObjectName(u"applybutton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.applybutton.sizePolicy().hasHeightForWidth())
        self.applybutton.setSizePolicy(sizePolicy1)
        self.applybutton.setMinimumSize(QSize(0, 35))

        self.verticalLayout_2.addWidget(self.applybutton)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.tab_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)

        self.verticalLayout_4.addWidget(self.label)

        self.cpp_combobox = QComboBox(self.tab_3)
        self.cpp_combobox.addItem("")
        self.cpp_combobox.addItem("")
        self.cpp_combobox.setObjectName(u"cpp_combobox")

        self.verticalLayout_4.addWidget(self.cpp_combobox)

        self.label_2 = QLabel(self.tab_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_4.addWidget(self.label_2)

        self.c_combobox = QComboBox(self.tab_3)
        self.c_combobox.addItem("")
        self.c_combobox.addItem("")
        self.c_combobox.setObjectName(u"c_combobox")

        self.verticalLayout_4.addWidget(self.c_combobox)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.applycompilebutton = QPushButton(self.tab_3)
        self.applycompilebutton.setObjectName(u"applycompilebutton")

        self.verticalLayout_4.addWidget(self.applycompilebutton)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.Decompiler_comboBox = QComboBox(self.tab_2)
        self.Decompiler_comboBox.addItem("")
        self.Decompiler_comboBox.addItem("")
        self.Decompiler_comboBox.setObjectName(u"Decompiler_comboBox")

        self.verticalLayout_3.addWidget(self.Decompiler_comboBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.Applydcompiler = QPushButton(self.tab_2)
        self.Applydcompiler.setObjectName(u"Applydcompiler")

        self.verticalLayout_3.addWidget(self.Applydcompiler)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.DBcombobox = QLabel(self.tab_4)
        self.DBcombobox.setObjectName(u"DBcombobox")
        self.DBcombobox.setFont(font)

        self.verticalLayout_5.addWidget(self.DBcombobox)

        self.DPcombobox = QComboBox(self.tab_4)
        self.DPcombobox.addItem("")
        self.DPcombobox.addItem("")
        self.DPcombobox.setObjectName(u"DPcombobox")

        self.verticalLayout_5.addWidget(self.DPcombobox)

        self.Runix_help_button = QPushButton(self.tab_4)
        self.Runix_help_button.setObjectName(u"Runix_help_button")
        self.Runix_help_button.setMaximumSize(QSize(100, 16777215))

        self.verticalLayout_5.addWidget(self.Runix_help_button)

        self.Resetsettings_button = QPushButton(self.tab_4)
        self.Resetsettings_button.setObjectName(u"Resetsettings_button")
        self.Resetsettings_button.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayout_5.addWidget(self.Resetsettings_button)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.applyrunixsetting_button = QPushButton(self.tab_4)
        self.applyrunixsetting_button.setObjectName(u"applyrunixsetting_button")

        self.verticalLayout_5.addWidget(self.applyrunixsetting_button)

        self.tabWidget.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget)

        SettingWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SettingWindow)
    # setupUi

    def retranslateUi(self, SettingWindow):
        SettingWindow.setWindowTitle(QCoreApplication.translate("SettingWindow", u"Runix-settings", None))
        self.Terminalcombobox.setItemText(0, QCoreApplication.translate("SettingWindow", u"Auto", None))
        self.Terminalcombobox.setItemText(1, QCoreApplication.translate("SettingWindow", u"Kitty", None))
        self.Terminalcombobox.setItemText(2, QCoreApplication.translate("SettingWindow", u"Konsole", None))
        self.Terminalcombobox.setItemText(3, QCoreApplication.translate("SettingWindow", u"Alacritty", None))
        self.Terminalcombobox.setItemText(4, QCoreApplication.translate("SettingWindow", u"Gnome-terminal", None))
        self.Terminalcombobox.setItemText(5, QCoreApplication.translate("SettingWindow", u"Gnome-console", None))
        self.Terminalcombobox.setItemText(6, QCoreApplication.translate("SettingWindow", u"Xfce-Terminal", None))

        self.applybutton.setText(QCoreApplication.translate("SettingWindow", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("SettingWindow", u"Default terminal", None))
        self.label.setText(QCoreApplication.translate("SettingWindow", u"C++ Compiler", None))
        self.cpp_combobox.setItemText(0, QCoreApplication.translate("SettingWindow", u"G++", None))
        self.cpp_combobox.setItemText(1, QCoreApplication.translate("SettingWindow", u"Clang++", None))

        self.label_2.setText(QCoreApplication.translate("SettingWindow", u"C Compiler", None))
        self.c_combobox.setItemText(0, QCoreApplication.translate("SettingWindow", u"Gcc", None))
        self.c_combobox.setItemText(1, QCoreApplication.translate("SettingWindow", u"Clang", None))

        self.applycompilebutton.setText(QCoreApplication.translate("SettingWindow", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("SettingWindow", u"Default compiler", None))
        self.Decompiler_comboBox.setItemText(0, QCoreApplication.translate("SettingWindow", u"Objdump", None))
        self.Decompiler_comboBox.setItemText(1, QCoreApplication.translate("SettingWindow", u"Retdec", None))

        self.Applydcompiler.setText(QCoreApplication.translate("SettingWindow", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("SettingWindow", u"Default decompiler/disassembler", None))
        self.DBcombobox.setText(QCoreApplication.translate("SettingWindow", u"Display Backend", None))
        self.DPcombobox.setItemText(0, QCoreApplication.translate("SettingWindow", u"X11", None))
        self.DPcombobox.setItemText(1, QCoreApplication.translate("SettingWindow", u"Wayland", None))

        self.Runix_help_button.setText(QCoreApplication.translate("SettingWindow", u"Help", None))
        self.Resetsettings_button.setText(QCoreApplication.translate("SettingWindow", u"Reset Settings", None))
        self.applyrunixsetting_button.setText(QCoreApplication.translate("SettingWindow", u"Apply", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("SettingWindow", u"Runix", None))
    # retranslateUi

