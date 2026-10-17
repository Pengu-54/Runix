# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'runix_flag_uiXxCTSx.ui'
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
from PyQt6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_FlagWindow(object):
    def setupUi(self, FlagWindow):
        if not FlagWindow.objectName():
            FlagWindow.setObjectName(u"FlagWindow")
        FlagWindow.resize(800, 350)
        FlagWindow.setMinimumSize(QSize(0, 350))
        FlagWindow.setMaximumSize(QSize(16777215, 350))
        FlagWindow.setMouseTracking(False)
        FlagWindow.setTabletTracking(False)
        FlagWindow.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.centralwidget = QWidget(FlagWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stdlineedit = QLineEdit(self.centralwidget)
        self.stdlineedit.setObjectName(u"stdlineedit")

        self.verticalLayout.addWidget(self.stdlineedit)

        self.Ilineedit = QLineEdit(self.centralwidget)
        self.Ilineedit.setObjectName(u"Ilineedit")
        self.Ilineedit.setDragEnabled(True)
        self.Ilineedit.setReadOnly(False)

        self.verticalLayout.addWidget(self.Ilineedit)

        self.includelineedit = QLineEdit(self.centralwidget)
        self.includelineedit.setObjectName(u"includelineedit")
        self.includelineedit.setClearButtonEnabled(False)

        self.verticalLayout.addWidget(self.includelineedit)

        self.lmcheckbox = QCheckBox(self.centralwidget)
        self.lmcheckbox.setObjectName(u"lmcheckbox")

        self.verticalLayout.addWidget(self.lmcheckbox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.cancelbutton = QPushButton(self.widget)
        self.cancelbutton.setObjectName(u"cancelbutton")

        self.horizontalLayout.addWidget(self.cancelbutton)

        self.savebutton = QPushButton(self.widget)
        self.savebutton.setObjectName(u"savebutton")

        self.horizontalLayout.addWidget(self.savebutton)


        self.verticalLayout.addWidget(self.widget)

        FlagWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FlagWindow)

        QMetaObject.connectSlotsByName(FlagWindow)
    # setupUi

    def retranslateUi(self, FlagWindow):
        FlagWindow.setWindowTitle(QCoreApplication.translate("FlagWindow", u"Flags", None))
        self.stdlineedit.setPlaceholderText(QCoreApplication.translate("FlagWindow", u"-std #Example c++20", None))
        self.Ilineedit.setText("")
        self.Ilineedit.setPlaceholderText(QCoreApplication.translate("FlagWindow", u"-I #Example /Home/User/Projects", None))
        self.includelineedit.setPlaceholderText(QCoreApplication.translate("FlagWindow", u"-include #Example Config.h", None))
        self.lmcheckbox.setText(QCoreApplication.translate("FlagWindow", u"-lm", None))
        self.cancelbutton.setText(QCoreApplication.translate("FlagWindow", u"Cancel", None))
        self.savebutton.setText(QCoreApplication.translate("FlagWindow", u"Save", None))
    # retranslateUi

