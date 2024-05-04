# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(724, 562)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionLog_viewer = QAction(MainWindow)
        self.actionLog_viewer.setObjectName(u"actionLog_viewer")
        self.actionGenomes = QAction(MainWindow)
        self.actionGenomes.setObjectName(u"actionGenomes")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.informationTab = QWidget()
        self.informationTab.setObjectName(u"informationTab")
        self.gridLayout = QGridLayout(self.informationTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileInformationTable = QTableWidget(self.informationTab)
        self.fileInformationTable.setObjectName(u"fileInformationTable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileInformationTable.sizePolicy().hasHeightForWidth())
        self.fileInformationTable.setSizePolicy(sizePolicy)
        self.fileInformationTable.setStyleSheet(u"")
        self.fileInformationTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileInformationTable.setAlternatingRowColors(True)
        self.fileInformationTable.setShowGrid(True)
        self.fileInformationTable.setGridStyle(Qt.DotLine)
        self.fileInformationTable.setSortingEnabled(False)
        self.fileInformationTable.setColumnCount(0)
        self.fileInformationTable.horizontalHeader().setVisible(False)
        self.fileInformationTable.horizontalHeader().setCascadingSectionResizes(False)
        self.fileInformationTable.horizontalHeader().setStretchLastSection(True)
        self.fileInformationTable.verticalHeader().setVisible(True)
        self.fileInformationTable.verticalHeader().setCascadingSectionResizes(False)
        self.fileInformationTable.verticalHeader().setMinimumSectionSize(30)
        self.fileInformationTable.verticalHeader().setDefaultSectionSize(30)
        self.fileInformationTable.verticalHeader().setHighlightSections(False)
        self.fileInformationTable.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.fileInformationTable, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.toCramButton = QPushButton(self.informationTab)
        self.toCramButton.setObjectName(u"toCramButton")

        self.horizontalLayout.addWidget(self.toCramButton)

        self.toWesButton = QPushButton(self.informationTab)
        self.toWesButton.setObjectName(u"toWesButton")

        self.horizontalLayout.addWidget(self.toWesButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.progressBar = QProgressBar(self.informationTab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)

        self.tabWidget.addTab(self.informationTab, "")
        self.analyzeTab = QWidget()
        self.analyzeTab.setObjectName(u"analyzeTab")
        self.analyzeTab.setEnabled(True)
        self.gridLayout_4 = QGridLayout(self.analyzeTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_5 = QGroupBox(self.analyzeTab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_3 = QGridLayout(self.groupBox_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_17 = QPushButton(self.groupBox_5)
        self.pushButton_17.setObjectName(u"pushButton_17")

        self.gridLayout_3.addWidget(self.pushButton_17, 1, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)

        self.pushButton_16 = QPushButton(self.groupBox_5)
        self.pushButton_16.setObjectName(u"pushButton_16")

        self.gridLayout_3.addWidget(self.pushButton_16, 0, 4, 1, 1)

        self.pushButton_18 = QPushButton(self.groupBox_5)
        self.pushButton_18.setObjectName(u"pushButton_18")

        self.gridLayout_3.addWidget(self.pushButton_18, 1, 4, 1, 1)

        self.pushButton_19 = QPushButton(self.groupBox_5)
        self.pushButton_19.setObjectName(u"pushButton_19")

        self.gridLayout_3.addWidget(self.pushButton_19, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.pushButton_15 = QPushButton(self.groupBox_5)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.gridLayout_3.addWidget(self.pushButton_15, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_5, 4, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 2, 2, 1, 1)

        self.groupBox_6 = QGroupBox(self.analyzeTab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_8 = QPushButton(self.groupBox_6)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_2.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.groupBox_6)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.groupBox_6)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_2.addWidget(self.pushButton_10)

        self.pushButton_11 = QPushButton(self.groupBox_6)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_2.addWidget(self.pushButton_11)


        self.gridLayout_4.addWidget(self.groupBox_6, 3, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.analyzeTab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_13 = QPushButton(self.groupBox_3)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.horizontalLayout_3.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.groupBox_3)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.horizontalLayout_3.addWidget(self.pushButton_14)


        self.gridLayout_4.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.analyzeTab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.pushButton_12 = QPushButton(self.groupBox_4)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.horizontalLayout_4.addWidget(self.pushButton_12)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.gridLayout_4.addWidget(self.groupBox_4, 2, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 5, 1, 1, 1)

        self.tabWidget.addTab(self.analyzeTab, "")
        self.extractTab = QWidget()
        self.extractTab.setObjectName(u"extractTab")
        self.gridLayout_2 = QGridLayout(self.extractTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 4, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.extractTab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_3 = QPushButton(self.groupBox)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.groupBox)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout_2.addWidget(self.pushButton_4)


        self.gridLayout_2.addWidget(self.groupBox, 4, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 6, 1, 1, 1)

        self.pushButton = QPushButton(self.extractTab)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 3, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.extractTab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_5 = QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_3.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.groupBox_2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.groupBox_2)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.verticalLayout_3.addWidget(self.pushButton_7)


        self.gridLayout_2.addWidget(self.groupBox_2, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 4, 0, 1, 1)

        self.tabWidget.addTab(self.extractTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 724, 21))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy1)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionLog_viewer)
        self.menuTools.addAction(self.actionGenomes)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WGSE - Genome sequencing data manipulation tool", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionLog_viewer.setText(QCoreApplication.translate("MainWindow", u"Log viewer", None))
        self.actionGenomes.setText(QCoreApplication.translate("MainWindow", u"Reference genomes", None))
        self.toCramButton.setText(QCoreApplication.translate("MainWindow", u"To CRAM", None))
        self.toWesButton.setText(QCoreApplication.translate("MainWindow", u"To WES", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.informationTab), QCoreApplication.translate("MainWindow", u"Information", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"VCF File(s)", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"Annotate", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Modify/Analyze", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"InDel", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"VarQC", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"SNP", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"BAM<-> FASTQ File", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Unalign", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Align", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"FASTP", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"FastQC", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Determine Haplogroups", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"Y Chromosome", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"Mitochondrial DNA", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Oral/Blood microbiome (Kaiju/CosmosID)", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Export unmapped reads", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analyzeTab), QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Mitocondrial", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (BAM)", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (FASTA)", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (VCF)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Microarray", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Y Chromosome", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Y and Mitochondrial (BAM)", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Y only (BAM)", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Y only (VCF)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.extractTab), QCoreApplication.translate("MainWindow", u"Extract", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

