#!/usr/bin/env python
# -*- coding: utf-8 -*-
#   Copyright (C) 2022-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of sound_source_id

#    sound_source_id is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    sound_source_id is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with sound_source_id.  If not, see <http://www.gnu.org/licenses/>.


import argparse, copy, fnmatch, logging, matplotlib, os, pickle, platform, random, scipy, signal, subprocess, sys, time, traceback
from sound_source_id.pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QFont, QIcon, QPainter, QDesktopServices
    from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QDesktopWidget, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
    from PyQt5.QtCore import QRect
    from PyQt5.QtCore import Qt, QEvent, QDate, QDateTime, QTime
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction, QFont, QIcon, QPainter, QDesktopServices
    from PyQt6.QtWidgets import QAbstractItemView, QApplication, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
    from PyQt6.QtCore import QRect
    from PyQt6.QtCore import Qt, QEvent, QDate, QDateTime, QTime

from numpy import sin, cos, pi, sqrt, abs, arange, zeros, mean, concatenate, convolve, angle, real, log2, log10, int_, linspace, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose
from numpy.fft import rfft, irfft, fft, ifft
from numpy import ceil, concatenate, floor, float32, int16, int32, mean, sqrt, transpose, zeros


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pysofaconventions as pysofa
from tempfile import mkstemp
from sound_source_id.audio_manager import*
from sound_source_id.sndlib import*
from sound_source_id.global_parameters import*
from sound_source_id.dialog_edit_preferences import*
from sound_source_id.dialog_edit_transducers import*
from sound_source_id import qrc_resources
from sound_source_id._version_info import*
from sound_source_id.utils import*
if platform.system() == 'Windows':
    import winsound

__version__ = sound_source_id_version
signal.signal(signal.SIGINT, signal.SIG_DFL)

if platform.system() == "Linux":
    try:
        import alsaaudio
    except ImportError:
        pass
try:
    import pyaudio
except ImportError:
    pass

local_dir = os.path.expanduser("~") +'/.local/share/data/sound_source_id/'
if os.path.exists(local_dir) == False:
    os.makedirs(local_dir)
stderrFile = os.path.expanduser("~") +'/.local/share/data/sound_source_id/sound_source_id_stderr_log.txt'

logging.basicConfig(filename=stderrFile,level=logging.DEBUG,)


#the except hook allows to see most startup errors in a window
#rather than the console
def excepthook(except_type, except_val, tbck):
    """ Show errors in message box"""
    # recover traceback
    tb = traceback.format_exception(except_type, except_val, tbck)
    def onClickSaveTbButton():
        ftow = QFileDialog.getSaveFileName(None, 'Choose where to save the traceback', "traceback.txt", 'All Files (*)')[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            fName = open(ftow, 'w')
            fName.write("".join(tb))
            fName.close()
    
    diag = QDialog(None, Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
    diag.window().setWindowTitle("Critical Error!")
    siz = QVBoxLayout()
    lay = QVBoxLayout()
    saveTbButton = QPushButton("Save Traceback", diag)
    saveTbButton.clicked.connect(onClickSaveTbButton)
    lab = QLabel("Sorry, something went wrong. The attached traceback can help you troubleshoot the problem: \n\n" + "".join(tb))
    lab.setMargin(10)
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    lab.setStyleSheet("QLabel { background-color: white }");
    lay.addWidget(lab)

    sc = QScrollArea()
    sc.setWidget(lab)
    siz.addWidget(sc) #SCROLLAREA IS A WIDGET SO IT NEEDS TO BE ADDED TO A LAYOUT

    buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

    buttonBox.accepted.connect(diag.accept)
    buttonBox.rejected.connect(diag.reject)
    siz.addWidget(saveTbButton)
    siz.addWidget(buttonBox)
    diag.setLayout(siz)
    diag.exec()

    timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
    logMsg = timeStamp + ''.join(tb)
    logging.debug(logMsg)


class applicationWindow(QMainWindow):
    """main window"""
    def __init__(self, prm):
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)
        self.prm = prm
        self.currBlock = 0
        #self.sampFreq = 48000
        #self.nbits = 32
        self.prm['version'] = __version__
        self.prm['builddate'] = sound_source_id_builddate
        
        self.saveResFile = ""
        self.listenerID = ""
        self.audioManager = audioManager(self)

        try:
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]
        ##if all previously stored transducers have been removed use the first of the new ones
        except:
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][0]
            
        self.trialRunning = False
        self.currLocale = prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.setWindowTitle(self.tr("sound_source_id"))
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
       
        self.f2_sizer = QVBoxLayout()
        self.f2_grid_sizer = QGridLayout()
        self.f2_sizer.addLayout(self.f2_grid_sizer)
        self.f2_sizer.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.f1 = QFrame()
        self.f1.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.f2 = QFrame()
        self.f2.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)

        self.statusBar()
        #MENU-----------------------------------
        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))

        loadPrmAction = QAction(self.tr('Load Parameters'), self)
        loadPrmAction.setShortcut('Ctrl+L')
        loadPrmAction.setStatusTip(self.tr('Load Parameters File'))
        loadPrmAction.triggered.connect(self.onClickLoadParameters)
        self.statusBar()
        self.fileMenu.addAction(loadPrmAction)

        exitButton = QAction(QIcon.fromTheme("application-exit", QIcon(':/exit')), self.tr('Exit'), self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip(self.tr('Exit application'))
        exitButton.triggered.connect(self.close)
        self.statusBar()
        self.fileMenu.addAction(exitButton)

        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.editPrefAction = QAction(self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.editTransducersAction = QAction(QIcon.fromTheme("audio-headphones", QIcon(":/audio-headphones")), self.tr('Transducers'), self)
        self.editMenu.addAction(self.editTransducersAction)
        self.editTransducersAction.triggered.connect(self.onEditTransducers)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowModulesDocAction = QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowModulesDocAction)
        self.onShowModulesDocAction.triggered.connect(self.onShowModulesDoc)

        self.onShowManualPdfAction = QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPdfAction)
        self.onShowManualPdfAction.triggered.connect(self.onShowManualPdf)

        self.onAboutAction = QAction(QIcon.fromTheme("help-about", QIcon(":/help-about")), self.tr('About sound_source_id'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)

        self.showPlayBtnAction = QAction(self.tr('Show Play Buttons'), self, checkable=True)
        self.editMenu.addAction(self.showPlayBtnAction)
        self.showPlayBtnAction.triggered.connect(self.onToggleShowPlayBtnAction)

        self.showRespBtnAction = QAction(self.tr('Show Response Buttons'), self, checkable=True)
        self.showRespBtnAction.setChecked(True)
        self.editMenu.addAction(self.showRespBtnAction)
        self.showRespBtnAction.triggered.connect(self.onToggleShowRespBtnAction)

        self.showRespLightAction = QAction(self.tr('Show Response Lights'), self, checkable=True)
        self.showRespLightAction.setChecked(True)
        self.editMenu.addAction(self.showRespLightAction)
        self.showRespLightAction.triggered.connect(self.onToggleShowRespLightAction)

        self.showControlPanelAction = QAction(self.tr('Show Control Panel'), self, checkable=True)
        self.showControlPanelAction.setChecked(True)
        self.editMenu.addAction(self.showControlPanelAction)
        self.showControlPanelAction.triggered.connect(self.onToggleShowControlPanelAction)

        n = 0
        self.listenerLabel = QLabel(self.tr('Listener:'), self)
        self.f2_grid_sizer.addWidget(self.listenerLabel, n, 0)
        self.listenerTF = QLineEdit("")
        self.f2_grid_sizer.addWidget(self.listenerTF, n, 1)
        self.listenerTF.editingFinished.connect(self.onListenerChange)


        if os.path.exists(prm["pref"]["default_prm_file"]):
            try:
                self.loadParameters(prm["pref"]["default_prm_file"])
            except:
                self.mode = "speakers"
                self.az_angles = np.array([-70, 70])
                self.elev_angles = np.array([0, 0])
                self.labels = ["1", "2"]
                self.channels = [1, 2]
                self.n_chan = 2
                self.n_blocks = 0
                self.stimListFile = ""
                self.randomizeTrialList = "true"
                self.demo_stim = ""
                self.demo_stim_lev = 0
                self.show()
                QMessageBox.warning(self, self.tr("Warning"), self.tr("There was an issue loading your default parameter file. It is likely to contain an error. Please select a new default parameters file and restart the program."))
                self.onEditPref()
        else:
            self.mode = "speakers"
            self.az_angles = np.array([-70, 70])
            self.elev_angles = np.array([0, 0])
            self.labels = ["1", "2"]
            self.channels = [1, 2]
            self.n_chan = 2
            self.n_blocks = 0
            self.stimListFile = ""
            self.randomizeTrialList = "true"
            self.demo_stim = ""
            self.demo_stim_lev = 0
            self.show()
            QMessageBox.warning(self, self.tr("Warning"), self.tr("The default parameters file could not be found. Please select a new default parameters file and restart the program."))
            self.onEditPref()


        self.statusButton = QPushButton(self.tr("Start"), self)
        self.f2_sizer.addWidget(self.statusButton)
        self.statusButton.clicked.connect(self.onClickStatusButton)
        self.statusButton.setStyleSheet('font-size: 14pt; font-weight: bold')

        self.loadPrmButton = QPushButton(self.tr("Load Parameters"), self)
        self.f2_sizer.addWidget(self.loadPrmButton)
        self.loadPrmButton.clicked.connect(self.onClickLoadParameters)
        self.loadPrmButton.setStyleSheet('font-size: 14pt; font-weight: bold')

        self.saveResultsButton = QPushButton(self.tr("Choose Results File"), self)
        self.f2_sizer.addWidget(self.saveResultsButton)
        self.saveResultsButton.clicked.connect(self.onClickSaveResultsButton)
        self.saveResultsButton.setStyleSheet('font-size: 14pt; font-weight: bold')
        self.saveResultsButton.show()

        self.resetButton = QPushButton(self.tr("Reset"), self)
        self.f2_sizer.addWidget(self.resetButton)
        self.resetButton.clicked.connect(self.onClickResetButton)
        self.resetButton.setStyleSheet('font-size: 14pt; font-weight: bold')

        self.runDemoButton = QPushButton(self.tr("Run Demo"), self)
        self.f2_sizer.addWidget(self.runDemoButton)
        self.runDemoButton.clicked.connect(self.onClickRunDemoButton)
        self.runDemoButton.setStyleSheet('font-size: 14pt; font-weight: bold')
        self.runDemoButton.show()

        self.f2.setLayout(self.f2_sizer)
        self.splitter.addWidget(self.f1)
        self.splitter.addWidget(self.f2)

        self.setCentralWidget(self.splitter)
        self.setGeometry(0, 0, int(screen.width()*3/4), screen.height())
        self.splitter.splitterMoved.connect(self.updateInterface)
        self.splitter.setSizes([int((5/6)*screen.width()), int((1/6)*screen.width())])

        self.setupInterface(clearPrev=False)
        
        self.audioManager.initializeAudio()
        self.show()
        self.updateInterface() #needed to get correct layout on Windows when program starts
        
    def onToggleShowPlayBtnAction(self):
        for pb in self.play_btn:
            if self.showPlayBtnAction.isChecked() == True:
                pb.show()
            else:
                pb.hide()
                
    def onToggleShowRespBtnAction(self):
        for pb in self.rsp_btn:
            if self.showRespBtnAction.isChecked() == True:
                pb.show()
            else:
                pb.hide()
                
    def onToggleShowRespLightAction(self):
        for lt in self.rsp_light:
            if self.showRespLightAction.isChecked() == True:
                lt.show()
            else:
                lt.hide()
    def onToggleShowControlPanelAction(self):
        if self.showControlPanelAction.isChecked() == True:
            self.f2.show()
        else:
            self.f2.hide()

    def loadParameters(self, fName):
        self.parametersFile = fName
        fStream = open(fName, 'r')
        allLines = fStream.readlines()
        fStream.close()
        self.az_angles = np.zeros(0)
        self.elev_angles = np.zeros(0)
        self.labels = []
        self.channels = []

        ## set default values to be overwritten if set in the parameters file
        self.resp_bt_wd = 40
        self.resp_bt_ht = 40
        self.play_bt_wd = 40
        self.play_bt_ht = 40
        self.resp_lt_wd = 40
        self.resp_lt_ht = 40
        self.resp_bt_rad_offset = 60
        self.play_bt_rad_offset = 80

        
        for i in range(len(allLines)):
            if allLines[i].split(':')[0].strip() == 'mode':
                self.mode = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'azimuths':
                az_angles_list = allLines[i].split(':')[1].strip().split(',')
                for li in az_angles_list:
                    self.az_angles = np.append(self.az_angles, int(li))
            elif allLines[i].split(':')[0].strip() == 'elevations':
                elevs_angles_list = allLines[i].split(':')[1].strip().split(',')
                for li in elevs_angles_list:
                    self.elev_angles = np.append(self.elev_angles, int(li))
            elif allLines[i].split(':')[0].strip() == 'labels':
                labels_list = allLines[i].split(':')[1].strip().split(',')
                for li in labels_list:
                    self.labels.append(li.strip())
            elif allLines[i].split(':')[0].strip() == 'channels':
                channels_list = allLines[i].split(':')[1].strip().split(',')
                for li in channels_list:
                    self.channels.append(int(li.strip()))
            elif allLines[i].split(':')[0].strip() == 'n_chan':
                self.n_chan = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'n_blocks':
                self.n_blocks = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'stim_list_file':
                self.stimListFile = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'randomize':
                self.randomizeTrialList = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'demo_stim':
                self.demo_stim = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'demo_stim_lev':
                self.demo_stim_lev = float(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'sofa_file_path':
                sofa_file_path = allLines[i].split(':')[1].strip()
                sofaFile = pysofa.SOFAFile(sofa_file_path, 'r')
                self.sourcePositions = sofaFile.getVariableValue('SourcePosition')
                self.HRIR_arr = sofaFile.getDataIR()
            elif allLines[i].split(':')[0].strip() == 'sofa_az_coords':
                self.sofa_az_coords = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'resp_bt_wd':
                self.resp_bt_wd = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'resp_bt_ht':
                self.resp_bt_ht = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'play_bt_wd':
                self.play_bt_wd = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'play_bt_ht':
                self.play_bt_ht = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'resp_lt_wd':
                self.resp_lt_wd = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'resp_lt_ht':
                self.resp_lt_ht = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'resp_bt_rad_offset':
                self.resp_bt_rad_offset = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'play_bt_rad_offset':
                self.play_bt_rad_offset = int(allLines[i].split(':')[1].strip())
                
        if len(self.elev_angles) == 0:
            self.elev_angles = np.zeros(len(self.az_angles)) #[0 for i in range(len(self.az_angles))]
            
        fDir = fName.split('/')[0:-1]
        fDir = "/".join([el for el in fDir]) + "/"
        os.chdir(fDir)
        self.stimList = pd.read_csv(self.stimListFile, sep=";")
        self.statusBar().showMessage(self.tr("Loaded ") + fName + self.tr(" parameter file"))

    def onClickLoadParameters(self):
        if self.statusButton.text() not in [self.tr("Start"), self.tr("Finished")]:
            reply = QMessageBox.warning(self, self.tr("Warning"), self.tr('This will stop the current test. Are you sure you want to proceed?'), QMessageBox.StandardButton.Yes | 
                                            QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
               self.resetTest() 
               fName = QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("All Files (*)"))[0]
               if len(fName) > 0: #if the user didn't press cancel
                   self.loadParameters(fName)
                   self.setupInterface(clearPrev=True)
        else:
            fName = QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("All Files (*)"))[0]
            if len(fName) > 0: #if the user didn't press cancel
                self.loadParameters(fName)
                self.setupInterface(clearPrev=True)
                
    def setupInterface(self, clearPrev):
        if clearPrev == True:
            for btn in self.rsp_btn:
                btn.deleteLater()
            for btn in self.play_btn:
                btn.deleteLater()
            for lgt in self.rsp_light:
                lgt.deleteLater()

        self.rsp_btn = []
        self.play_btn = []
        self.rsp_light = []
        for i in range(len(self.az_angles)):
            self.rsp_btn.append(QPushButton(self.labels[i], parent = self.f1))
            self.rsp_btn[i].clicked.connect(self.on_click_response_button)

            self.play_btn.append(QPushButton('>'+self.labels[i], parent = self.f1))
            self.play_btn[i].clicked.connect(self.on_click_play_button)
            self.rsp_light.append(responseLight(self.f1, self.prm))

        self.updateInterface()
        

    def updateInterface(self):
        base_rad = np.minimum(int(self.f1.height()/2), int(self.f1.width()/2))-45
        rad_rl = base_rad # response light radius
        rad_rb = rad_rl - self.resp_bt_rad_offset #60 #response button radius
        rad_pb = rad_rb - self.play_bt_rad_offset #60  #play button radius

        dxl = []; dyl = []
        dx_pb = []; dy_pb = []
        x_offset = 50
        y_offset = 10
        for i in range(len(self.az_angles)):
            #angle = deg2rad(self.az_angles[i]+90)
            # dx = int(rad_rb*np.cos(angle)*np.cos(elev))+rad_rl+x_offset
            # dy = -int(rad_rb*np.sin(angle)*np.cos(elev))+rad_rl+y_offset
            angle = deg2rad(self.az_angles[i])
            elev = deg2rad(self.elev_angles[i])
            dx = int(rad_rb*np.sin(angle)*np.cos(elev))+rad_rl+x_offset
            dy = -int(rad_rb*np.cos(angle)*np.cos(elev))+rad_rl+y_offset

            dxl.append(int(rad_rl*np.sin(angle)*np.cos(elev))+rad_rl+x_offset)
            dyl.append(-int(rad_rl*np.cos(angle)*np.cos(elev))+rad_rl+y_offset)
            dx_pb.append(int(rad_pb*np.sin(angle)*np.cos(elev))+rad_rl+x_offset)
            dy_pb.append(-int(rad_pb*np.cos(angle)*np.cos(elev))+rad_rl+y_offset)

            self.rsp_light[i].setGeometry(QRect(dxl[i], dyl[i], self.resp_lt_wd, self.resp_lt_ht))
            self.rsp_btn[i].setGeometry(QRect(dx, dy, self.resp_bt_wd, self.resp_bt_ht))
            self.play_btn[i].setGeometry(QRect(dx_pb[i], dy_pb[i], self.play_bt_wd, self.play_bt_ht))

            self.rsp_btn[i].move(dx, dy)
            self.play_btn[i].move(dx_pb[i], dy_pb[i])
            self.rsp_light[i].move(dxl[i], dyl[i])
            
            if self.showRespBtnAction.isChecked() == True:
                self.rsp_btn[i].show()
            else:
                self.rsp_btn[i].hide()
                
            if self.showRespLightAction.isChecked() == True:
                self.rsp_light[i].show()
            else:
                self.rsp_light[i].hide()
                
            if self.showPlayBtnAction.isChecked() == True:
                self.play_btn[i].show()
            else:
                self.play_btn[i].hide()

    def resizeEvent(self, event):
        self.updateInterface()
        #self.splitter.setSizes([int((5/6)*self.width()), int((1/6)*self.width())])
        QMainWindow.resizeEvent(self, event)


    def initializeResultsFile(self, ftow):
        self.saveResPath = ftow #file where results are saved
        self.saveResDir = os.path.dirname(str(ftow)) + '/' #directory where results are saved
        self.saveResFile = open(self.saveResPath, "w")
        self.saveResFile.write("listener" + self.prm['pref']['csvSeparator'] +
                               "condition" + self.prm['pref']['csvSeparator'] +
                               "block" + self.prm['pref']['csvSeparator'] +
                               "trial" + self.prm['pref']['csvSeparator'] +
                               "azimuth_angle" + self.prm['pref']['csvSeparator'] +
                               "elevation_angle" + self.prm['pref']['csvSeparator'] +
                               "response_azimuth" + self.prm['pref']['csvSeparator'] +
                               "response_elevation" + self.prm['pref']['csvSeparator'] +
                               "azimuth_error" + self.prm['pref']['csvSeparator'] +
                               "elevation_error" + self.prm['pref']['csvSeparator'] +
                               "azimuth_angle_remapped" + self.prm['pref']['csvSeparator'] +
                               "response_azimuth_remapped" + self.prm['pref']['csvSeparator'] +
                               "azimuth_angle_flip" + self.prm['pref']['csvSeparator'] +
                               "response_azimuth_flip" + self.prm['pref']['csvSeparator'] +
                               "azimuth_error_flip" + self.prm['pref']['csvSeparator'] +
                               "front_back" + self.prm['pref']['csvSeparator'] +
                               "sound_file" + self.prm['pref']['csvSeparator'] +
                               "base_level" + self.prm['pref']['csvSeparator'] +
                               "rove" + self.prm['pref']['csvSeparator'] +
                               "actual_level" + self.prm['pref']['csvSeparator'] +
                               "date" + self.prm['pref']['csvSeparator'] +
                               "time\n")


    def chooseResFile(self):
        satisfied = 0
        while satisfied == 0:
            ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), os.path.expanduser("~"), self.tr('csv (*.csv)'), "")[0]
            if ftow != "":
                if fnmatch.fnmatch(ftow, '*.csv') == False:
                    ftow = ftow + '.csv'
                if os.path.exists(ftow) == True:
                    reply = QMessageBox.warning(self, self.tr("Warning"), self.tr('File ') + ftow + self.tr('already exists. Do you want to overwrite it?'), QMessageBox.StandardButton.Yes |
                                                QMessageBox.StandardButton.No,
                                                QMessageBox.StandardButton.Yes)
                    if reply == QMessageBox.StandardButton.Yes:
                        satisfied = 1
                        return ftow
                else:
                    satisfied = 1
                    return ftow
            else:
                satisfied = 1
                return ftow        
              
    def onClickSaveResultsButton(self):
        if self.currBlock == 0:
            ftow = self.chooseResFile()
            if ftow != "":
                self.initializeResultsFile(ftow)
        else:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("The results file cannot be changed while a test is running. Reset the test and then choose a new results file."))
  
    def onClickStatusButton(self):
        if self.currBlock == 0:
            if self.saveResFile == "":
                ftow = self.chooseResFile()
                if ftow != "":
                    self.initializeResultsFile(ftow)
                else:
                    QMessageBox.warning(self, self.tr("Warning"), self.tr("You need to select a file where to save the results to proceed"))
                return
            
            if self.listenerID == "":
                msg = self.tr("Please, enter the listener's name:") 
                text, ok = QInputDialog.getText(self, self.tr("Input Dialog:") , msg)
                if ok:
                    self.listenerID = text
                    self.listenerTF.setText(self.listenerID)
                return

            self.currBlock = 1
            self.statusButton.setText(self.tr("Running"))
            self.do_block()
          
        elif self.currBlock > 0 and self.currBlock < self.n_blocks:
            self.statusButton.setText(self.tr("Running"))
            self.currBlock = self.currBlock + 1
            self.do_block()

    def onClickResetButton(self):
        if self.statusButton.text() not in [self.tr("Start"), self.tr("Finished")]:
            reply = QMessageBox.warning(self, self.tr("Warning"), self.tr('This will stop the current test. Are you sure you want to proceed?'), QMessageBox.StandardButton.Yes | 
                                            QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if reply == QMessageBox.StandardButton.Yes:
               self.resetTest() 
               
        else:
           self.resetTest()
           
    def resetTest(self):
         self.trialRunning = False
         self.currBlock = 0
         self.saveResFile = ""
         self.statusButton.setText(self.tr("Start"))
         self.listenerID = ""
         self.listenerTF.setText(self.listenerID)
         
    def onClickRunDemoButton(self):
        if self.trialRunning == True:
            return
        self.trialRunning = True
        for i in range(len(self.az_angles)):
            if self.mode == "speakers":
                self.prep_sound_speakers(self.demo_stim, i+1, self.demo_stim_lev)
            elif self.mode == "headphones":
                self.prep_sound_headphones(self.demo_stim, self.demo_stim_lev, self.az_angles[i], self.elev_angles[i])
            self.rsp_light[i].setStatus('neutral')
            self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav") 
            self.rsp_light[i].setStatus('off')
            time.sleep(0.5)
        QApplication.processEvents()
        self.trialRunning = False
        
    def do_block(self):
        self.nTrials = self.stimList.shape[0]
        if self.randomizeTrialList == "true":
            self.stimList = self.stimList.sample(frac=1)
        self.currTrialN = 1
        self.do_trial()
        
    def do_trial(self):
        self.trialRunning = True

        self.curr_az = self.stimList['az_angle'].values[self.currTrialN-1]
        self.curr_elev = self.stimList['elev_angle'].values[self.currTrialN-1]
        #self.currIdx = self.az_angles.index(self.curr_az)
        self.currIdx = np.where((self.az_angles == self.curr_az) & (self.elev_angles == self.curr_elev))[0][0]
        if self.mode == "speakers":
            self.curr_chan = self.channels[self.currIdx]
        self.curr_stim_file = self.stimList['sound_file'].values[self.currTrialN-1]
        self.curr_stim_lev = self.stimList['level'].values[self.currTrialN-1]
        self.curr_rove = self.stimList['roving'].values[self.currTrialN-1]
        self.curr_lev = self.curr_stim_lev + random.uniform(-self.curr_rove, self.curr_rove)
        self.giveFeedback = self.stimList['feedback'].values[self.currTrialN-1]
        self.curr_cnd = self.stimList['condition'].values[self.currTrialN-1]

        if self.mode == "speakers":
            self.prep_sound_speakers(self.curr_stim_file, self.curr_chan, self.curr_lev)
        elif self.mode == "headphones":
            self.prep_sound_headphones(self.curr_stim_file, self.curr_lev, self.curr_az, self.curr_elev)
        self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav")

        QApplication.processEvents()
        self.trialRunning = False

    def on_click_play_button(self):
        try:
            buttonClicked = self.play_btn.index(self.sender())+1
        except:
            buttonClicked = 0

        ang = self.az_angles[buttonClicked-1]
        elev = self.elev_angles[buttonClicked-1]
        if self.mode == "speakers":
            chan = self.channels[buttonClicked-1]
        stim_file = self.demo_stim 
        lev = self.demo_stim_lev

        if self.mode == "speakers":
            self.prep_sound_speakers(stim_file, chan, lev)
        elif self.mode == "headphones":
            self.prep_sound_headphones(stim_file, lev, ang, elev)
        self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav")

    def prep_sound_speakers(self, stim_file, chan, lev):
        curr_stim_mono, sf, nbits = self.audioManager.loadWavFile(stim_file, lev, self.maxLevel, channel="Original")
        self.sampFreq = sf
        self.nbits = nbits

        if curr_stim_mono.ndim > 1:
            curr_stim_mono = curr_stim_mono[:,0]
        curr_stim_mono  = curr_stim_mono.reshape(curr_stim_mono.shape[0], 1)

        self.curr_stim_multi = np.zeros((curr_stim_mono.shape[0], self.n_chan))
        self.curr_stim_multi[:, chan-1] = curr_stim_mono[:,0]
        if self.prm["pref"]["sound"]["prependSilence"] > 0:
            duration = self.prm["pref"]["sound"]["prependSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * sf))
            silenceToPrepend = zeros((nSamples, self.n_chan))
            self.curr_stim_multi = concatenate((silenceToPrepend, self.curr_stim_multi), axis=0)
        if self.prm["pref"]["sound"]["appendSilence"] > 0:
            duration = self.prm["pref"]["sound"]["appendSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * sf))
            silenceToAppend = zeros((nSamples, self.n_chan))
            self.curr_stim_multi = concatenate((self.curr_stim_multi, silenceToAppend), axis=0)

    def prep_sound_headphones(self, stim_file, lev, az_ang, elev_ang=0):
        curr_stim_mono, sf, nbits = self.audioManager.loadWavFile(stim_file, lev, self.maxLevel, channel="Original")
        self.sampFreq = sf
        self.nbits = nbits

        if curr_stim_mono.ndim > 1:
            curr_stim_mono = curr_stim_mono[:,0]
        curr_stim_mono  = curr_stim_mono.reshape(curr_stim_mono.shape[0], 1)

        if self.sofa_az_coords == "anticlockwise":
            az_ang = -az_ang
        ref_idx, self.actual_az, ref_actual_elev, ref_az_err, ref_elev_err, ref_db_coord_az, ref_db_coord_elev = get_hrir_idx(az_ang, elev_ang, self.sourcePositions)
        if self.sofa_az_coords == "anticlockwise":
            self.actual_az = -self.actual_az
        ref_hrir = self.HRIR_arr[ref_idx, :, :]
        snd_L = scipy.signal.fftconvolve(curr_stim_mono[:,0], ref_hrir[0])
        snd_R = scipy.signal.fftconvolve(curr_stim_mono[:,0], ref_hrir[1])
        self.curr_stim_multi = np.zeros((snd_L.shape[0], self.n_chan))
        self.curr_stim_multi[:,0] = snd_L
        self.curr_stim_multi[:,1] = snd_R
            
    def on_click_response_button(self):
        #the try-except is here because when the interface is updating between blocks
        #the sender may be missing (participants press multiple times response button when interface is changing)
        try:
            buttonClicked = self.rsp_btn.index(self.sender())+1
        except:
            buttonClicked = 0
        self.sortResponse(buttonClicked)

    def sortResponse(self, buttonClicked):
        if buttonClicked == 0: #0 is not a response option
            return
        if self.statusButton.text() != self.tr("Running"):
            return
        if self.trialRunning == True: # do not accept responses while the trial is running
            return

        rsp_az = self.az_angles[buttonClicked-1]
        rsp_elev = self.elev_angles[buttonClicked-1]

        if self.giveFeedback == True:
            if rsp_az == self.curr_az and rsp_elev == self.curr_elev:
                self.rsp_light[self.currIdx].giveFeedback('correct', '')
            else:
                self.rsp_light[self.currIdx].giveFeedback('incorrect', '')
       
            
        currTime = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.ShortFormat)) 
        currDate = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.ShortFormat)) 

        raw_az_err = self.curr_az-rsp_az
        poss = np.array([raw_az_err, raw_az_err-360, raw_az_err+360])
        az_err_idx = np.where(np.abs(poss) == np.min(np.abs(poss)))[0][0]
        az_err = poss[az_err_idx]
        
        raw_elev_err = self.curr_elev-rsp_elev

        if self.curr_az < 0:
            az_angle_remapped = self.curr_az + 360
        else:
            az_angle_remapped = copy.copy(self.curr_az)
            
        if rsp_az < 0:
            resp_az_remapped = rsp_az + 360
        else:
            resp_az_remapped = copy.copy(rsp_az)
            
        if az_angle_remapped > 90 and az_angle_remapped <= 180:
            az_angle_flip = 180 - az_angle_remapped
        elif az_angle_remapped > 180 and az_angle_remapped < 270:
            az_angle_flip = 360 - az_angle_remapped + 180
        else:
            az_angle_flip = copy.copy(az_angle_remapped)

        if resp_az_remapped > 90 and resp_az_remapped <= 180:
            resp_az_flip = 180 - resp_az_remapped
        elif resp_az_remapped > 180 and resp_az_remapped < 270:
            resp_az_flip = 360 - resp_az_remapped + 180
        else:
            resp_az_flip = copy.copy(resp_az_remapped)

        raw_az_err_flip = az_angle_flip - resp_az_flip
        poss_flip = np.array([raw_az_err_flip, raw_az_err_flip-360, raw_az_err_flip+360])
        az_err_idx_flip = np.where(np.abs(poss_flip) == np.min(np.abs(poss_flip)))[0][0]
        az_err_flip = poss_flip[az_err_idx_flip]

        if np.abs(az_err) > np.abs(az_err_flip):
            front_back = 1
        else:
            front_back = 0
        
        #listener
        self.saveResFile.write(self.listenerID + self.prm['pref']["csvSeparator"])
        #condition
        self.saveResFile.write(str(self.curr_cnd) + self.prm['pref']["csvSeparator"])
        #block
        self.saveResFile.write(str(self.currBlock) + self.prm['pref']["csvSeparator"])
        #trial
        self.saveResFile.write(str(self.currTrialN) + self.prm['pref']["csvSeparator"])
        #azimuth angle
        self.saveResFile.write(str(self.curr_az) + self.prm['pref']["csvSeparator"])
        #elevation angle
        self.saveResFile.write(str(self.curr_elev) + self.prm['pref']["csvSeparator"])
        #response azimuth
        self.saveResFile.write(str(rsp_az) + self.prm['pref']["csvSeparator"])
        #response elevation
        self.saveResFile.write(str(rsp_elev) + self.prm['pref']["csvSeparator"])
        #azimuth error
        self.saveResFile.write(str(az_err) + self.prm['pref']["csvSeparator"])
        #elevation error
        self.saveResFile.write(str(raw_elev_err) + self.prm['pref']["csvSeparator"])

        
        #azimuth angle remapped
        self.saveResFile.write(str(az_angle_remapped) + self.prm['pref']["csvSeparator"])
        #response azimuth remapped
        self.saveResFile.write(str(resp_az_remapped) + self.prm['pref']["csvSeparator"])
        #azimuth angle flipped
        self.saveResFile.write(str(az_angle_flip) + self.prm['pref']["csvSeparator"])
        #response azimuth flipped
        self.saveResFile.write(str(resp_az_flip) + self.prm['pref']["csvSeparator"])
        #azimuth error flip
        self.saveResFile.write(str(az_err_flip) + self.prm['pref']["csvSeparator"])
        #front/back
        self.saveResFile.write(str(front_back) + self.prm['pref']["csvSeparator"])
        

        #sound file
        self.saveResFile.write(self.curr_stim_file + self.prm['pref']["csvSeparator"])
        #base level
        self.saveResFile.write(str(self.curr_stim_lev) + self.prm['pref']["csvSeparator"])
        #rove
        self.saveResFile.write(str(self.curr_rove) + self.prm['pref']["csvSeparator"])
        #level
        self.saveResFile.write(str(self.curr_lev) + self.prm['pref']["csvSeparator"])
        #date
        self.saveResFile.write(currDate + self.prm['pref']["csvSeparator"])
        #time
        self.saveResFile.write(currTime)
        self.saveResFile.write('\n')
        self.saveResFile.flush()

        if self.currTrialN == self.nTrials:
            if self.currBlock < self.n_blocks:
                self.statusButton.setText(self.tr("Run Block"))
            else:
                self.saveResFile.close()
                self.statusButton.setText(self.tr("Finished"))
                dats = pd.read_csv(self.saveResPath, sep=self.prm['pref']["csvSeparator"])

                rms_err = dats.groupby("listener").agg({'azimuth_error' : lambda x: rms_fun(x), 'elevation_error' : lambda x: rms_fun(x), 'azimuth_error_flip' : lambda x: rms_fun(x)})
                rms_err_by_block = dats.groupby(["listener", "block"]).agg({'azimuth_error' : lambda x: rms_fun(x), 'elevation_error' : lambda x: rms_fun(x), 'azimuth_error_flip' : lambda x: rms_fun(x)})
                rms_err_by_cnd = dats.groupby(["listener", "condition"]).agg({'azimuth_error' : lambda x: rms_fun(x), 'elevation_error' : lambda x: rms_fun(x), 'azimuth_error_flip' : lambda x: rms_fun(x)})
                rms_err_by_cnd_block = dats.groupby(["listener", "condition", "block"]).agg({'azimuth_error' : lambda x: rms_fun(x), 'elevation_error' : lambda x: rms_fun(x), 'azimuth_error_flip' : lambda x: rms_fun(x)})

                rms_err =  rms_err.rename(columns={"azimuth_error": "rms_azimuth_err", "elevation_error": "rms_elevation_err", "azimuth_error_flip": "rms_azimuth_err_flip"})
                rms_err_by_block =  rms_err_by_block.rename(columns={"azimuth_error": "rms_azimuth_err", "elevation_error": "rms_elevation_err", "azimuth_error_flip": "rms_azimuth_err_flip"})
                rms_err_by_cnd = rms_err_by_cnd.rename(columns={"azimuth_error": "rms_azimuth_err", "elevation_error": "rms_elevation_err", "azimuth_error_flip": "rms_azimuth_err_flip"})
                rms_err_by_cnd_block = rms_err_by_cnd_block.rename(columns={"azimuth_error": "rms_azimuth_err", "elevation_error": "rms_elevation_err", "azimuth_error_flip": "rms_azimuth_err_flip"})

                rms_err_nofb = dats[dats['front_back'] == 0].groupby("listener").agg({'azimuth_error' : lambda x: rms_fun(x)})
                rms_err_nofb_by_block = dats[dats['front_back'] == 0].groupby(["listener", "block"]).agg({'azimuth_error' : lambda x: rms_fun(x)})
                rms_err_nofb_by_cnd = dats[dats['front_back'] == 0].groupby(["listener", "condition"]).agg({'azimuth_error' : lambda x: rms_fun(x)})
                rms_err_nofb_by_cnd_block = dats[dats['front_back'] == 0].groupby(["listener", "condition", "block"]).agg({'azimuth_error' : lambda x: rms_fun(x)})

                
                rms_err_nofb =  rms_err_nofb.rename(columns={"azimuth_error": "az_rms_err_no_FB"})
                rms_err_nofb_by_block =  rms_err_nofb_by_block.rename(columns={"azimuth_error": "az_rms_err_no_FB"})
                rms_err_nofb_by_cnd =  rms_err_nofb_by_cnd.rename(columns={"azimuth_error": "az_rms_err_no_FB"})
                rms_err_nofb_by_cnd_block =  rms_err_nofb_by_cnd_block.rename(columns={"azimuth_error": "az_rms_err_no_FB"})

                rms_err = pd.concat([rms_err, rms_err_nofb], axis=1)
                rms_err_by_block = pd.concat([rms_err_by_block, rms_err_nofb_by_block], axis=1)
                rms_err_by_cnd = pd.concat([rms_err_by_cnd, rms_err_nofb_by_cnd], axis=1)
                rms_err_by_cnd_block = pd.concat([rms_err_by_cnd_block, rms_err_nofb_by_cnd_block], axis=1)

                fb_err = dats.groupby("listener").agg({'front_back' : lambda x: np.sum(x)/len(x)})
                fb_err_by_block = dats.groupby(["listener", "block"]).agg({'front_back' : lambda x: np.sum(x)/len(x)})
                fb_err_by_cnd = dats.groupby(["listener", "condition"]).agg({'front_back' : lambda x: np.sum(x)/len(x)})
                fb_err_by_cnd_block = dats.groupby(["listener", "condition", "block"]).agg({'front_back' : lambda x: np.sum(x)/len(x)}) 

                rms_err.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err.csv", sep=";")
                fb_err.to_csv(self.saveResPath.split(".csv")[0] + "_" + "front-back_err.csv", sep=";")
                if rms_err_by_block.empty == False and np.unique(dats['block']) > 1:
                    rms_err_by_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_block.csv", sep=";")
                    fb_err_by_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "front-back_err_by_block.csv", sep=";")
                if rms_err_by_cnd.empty == False:
                    rms_err_by_cnd.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_cnd.csv", sep=";")
                    fb_err_by_cnd.to_csv(self.saveResPath.split(".csv")[0] + "_" + "front-back_err_by_cnd.csv", sep=";")
                if rms_err_by_cnd_block.empty == False:
                    rms_err_by_cnd_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_cnd_block.csv", sep=";")
                    fb_err_by_cnd_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "front-back_err_by_cnd_block.csv", sep=";")

                response_azimuth_remapped_closest = np.zeros(dats.shape[0])
                for i in range(dats.shape[0]):
                    errs = dats['azimuth_angle_remapped'][i]-dats['response_azimuth_remapped'][i]
                    poss = np.array([dats['response_azimuth_remapped'][i], dats['response_azimuth_remapped'][i]-360, dats['response_azimuth_remapped'][i]+360])
                    poss_errs = np.array([errs, errs-360, errs+360])
                    az_err_idx = np.where(np.abs(poss_errs) == np.min(np.abs(poss_errs)))[0][0]
                    response_azimuth_remapped_closest[i] = poss[az_err_idx]
                dats['response_azimuth_remapped_closest'] = response_azimuth_remapped_closest

                #matplotlib.rcParams['backend'] = "QtAgg"
                plt.ioff()
                plt.scatter(dats['azimuth_angle_remapped'], dats['response_azimuth_remapped_closest'])
                plt.savefig(self.saveResPath.split(".csv")[0] + "_scatter.pdf")
                    
        else:
            self.currTrialN = self.currTrialN +1
            self.do_trial()

    def onListenerChange(self):
        self.listenerID = self.listenerTF.text()
    
    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]
            self.audioManager.initializeAudio()
            
    def onEditTransducers(self):
        dialog = transducersDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            ##if all previously stored transducers have been removed use the first of the new ones
            try:
                currTransducerIdx = self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])
            except:
                currTransducerIdx = 0
            self.prm["pref"]["sound"]["transducers"] = self.prm["transducers"]["transducersChoices"][currTransducerIdx]
            self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]

            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]

    def onShowManualPdf(self):
        fileToOpen = os.path.abspath(self.prm['rootDirectory']) + '/doc/_build/latex/sound_source_id.pdf'
        print(fileToOpen)
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onShowModulesDoc(self):
        fileToOpen = os.path.abspath(self.prm['rootDirectory']) + '/doc/_build/html/index.html'
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))

    def createAppShortcut(self):
        from pyshortcuts import make_shortcut
        make_shortcut(script="sound_source_id", name='sound_source_id', icon=os.path.dirname(__file__)+"icons/point-right.ico", terminal=False, executable=None)

    def onAbout(self):
        qt_compiled_ver = QtCore.QT_VERSION_STR
        qt_runtime_ver = QtCore.qVersion()
        qt_pybackend_ver = QtCore.PYQT_VERSION_STR
        qt_pybackend = "PyQt"


        QMessageBox.about(self, self.tr("About sound_source_id"),
                              self.tr("""<b>sound_source_id - Python app for sound localization experiments</b> <br>
                              - version: {0}; <br>
                              - build date: {1} <br>
                              <p> Copyright &copy; 2022-2023 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
                              All rights reserved. <p>
                              This program is free software: you can redistribute it and/or modify
                              it under the terms of the GNU General Public License as published by
                              the Free Software Foundation, either version 3 of the License, or
                              (at your option) any later version.
                              <p>
                              This program is distributed in the hope that it will be useful,
                              but WITHOUT ANY WARRANTY; without even the implied warranty of
                              MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                              GNU General Public License for more details.
                              <p>
                              You should have received a copy of the GNU General Public License
                              along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>
                              <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(__version__, self.prm['builddate'], platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))

def get_hrir_idx(az, elev, sourcePositions):
    az = az % 360
    elev = elev % 360
    requested_az = az
    requested_elev = elev
    flip_az_flag = False
    if elev > 90 and elev <= 270:
        elev = 180 - elev #and flip az
        flip_az_flag = True
    elif elev > 270:
        elev = elev - 360 #do not flip az

    if flip_az_flag == True:
        if az >= 0 and az <= 180:
            az = 180 - az
        elif az > 180 and az <= 360:
            az = 180 - az + 360

    selec_arr = np.sqrt((sourcePositions[:,0] - az)**2 + (sourcePositions[:,1]-elev)**2)
    idx_arr = np.where(selec_arr == np.min(selec_arr))
    idx = np.random.choice(idx_arr[0], 1)[0] #if there are two or more equidistant points pick one at random

    actual_az_db_coord = sourcePositions[idx, 0]
    actual_elev_db_coord = sourcePositions[idx, 1]

    if flip_az_flag == True:
        actual_elev = 180 - actual_elev_db_coord 
        if actual_az_db_coord >= 0 and actual_az_db_coord <= 180:
            actual_az = 180 - actual_az_db_coord
        elif actual_az_db_coord > 180 and actual_az_db_coord <= 360:
            actual_az = 180 - actual_az_db_coord + 360
    else:
        actual_elev = actual_elev_db_coord % 360
        actual_az = actual_az_db_coord

    az_err = actual_az - requested_az 
    elev_err = actual_elev - requested_elev 
    # print("===============================")
    # print("requested az: " + str(requested_az))
    # print("actual az: " + str(actual_az))
    # print("az_err: " + str(az_err))
    # print("requested elev: " + str(requested_elev))
    # print("actual_elev: " + str(actual_elev))
    # print("elev_err: "+str(elev_err))
    # print("actual_az_db_coord: " + str(actual_az_db_coord))
    # print("actual_elev_db_coord: " + str(actual_elev_db_coord))

    return idx, actual_az, actual_elev, az_err, elev_err, actual_az_db_coord, actual_elev_db_coord

            
class responseLight(QWidget):
    def __init__(self, parent, prm):
        super(responseLight, self).__init__(parent)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
        #                                QSizePolicy.Expanding))
        #self.cw = self.parent().parent() #control window
        self.RL_prm = prm
        self.correctLightColor = QColor(*self.RL_prm["pref"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.RL_prm["pref"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.RL_prm["pref"]["neutralLightColor"])
        self.offLightColor = QColor(*self.RL_prm["pref"]["offLightColor"])
        
        self.borderColor = Qt.GlobalColor.black
        self.lightColor = self.offLightColor#Qt.black
        self.feedbackText = ""
        self.responseLightType = self.tr("Light & Text") #this is just for inizialization purposes
        self.penColor = QColor(255,255,255) #this is just for inizialization purposes
        

        self.correctSmiley = QIcon.fromTheme("face-smile", QIcon(":/face-smile"))
        self.incorrectSmiley = QIcon.fromTheme("face-sad", QIcon(":/face-sad"))
        self.neutralSmiley = QIcon.fromTheme("face-plain", QIcon(":/face-plain"))
        self.offSmiley = QIcon() #create just a null icon
        self.feedbackSmiley = self.offSmiley
        
    def giveFeedback(self, feedback, feedbackText):
        self.feedbackText = feedbackText
        ##currBlock = 'b'+ str(self.RL_prm['currentBlock'])
        self.responseLightType = self.tr("Light & Text") ##self.parent().self.RL_prm[currBlock]['responseLightType']
        self.setStatus(feedback)
        self.parent().repaint()
        QApplication.processEvents()
        time.sleep(self.RL_prm["pref"]["responseLightDuration"]/1000) ##self.parent().self.RL_prm["pref"]
        self.setStatus('off')
        self.parent().repaint()
        QApplication.processEvents()
        
    def setStatus(self, status):
        self.correctLightColor = QColor(*self.RL_prm["pref"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.RL_prm["pref"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.RL_prm["pref"]["neutralLightColor"])
        self.offLightColor = QColor(*self.RL_prm["pref"]["offLightColor"])
        if self.responseLightType in [self.tr("Light"), self.tr("Light & Text"), self.tr("Light & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.lightColor = self.correctLightColor#Qt.green
            elif status == 'incorrect':
                self.lightColor = self.incorrectLightColor #Qt.red
            elif status == 'neutral':
                self.lightColor = self.neutralLightColor #Qt.white
            elif status == 'off':
                self.lightColor = self.offLightColor #Qt.black
        if self.responseLightType in [self.tr("Text"), self.tr("Light & Text"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                # if self.RL_prm["pref"]["correctTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetCorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.RL_prm['rbTrans'].translate('rb', self.RL_prm["pref"]["correctTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["correctTextColor"])
            elif status == 'incorrect':
                # if self.RL_prm["pref"]["incorrectTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetIncorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.RL_prm['rbTrans'].translate('rb', self.RL_prm["pref"]["incorrectTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["incorrectTextColor"])
            elif status == 'neutral':
                # if self.RL_prm["pref"]["neutralTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetNeutralTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.RL_prm["pref"]["neutralTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["neutralTextColor"])
            elif status == 'off':
                # if self.RL_prm["pref"]["offTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetOffTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.RL_prm["pref"]["offTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["offTextColor"])
        if self.responseLightType in [self.tr("Smiley"), self.tr("Light & Smiley"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.feedbackSmiley = self.correctSmiley
            elif status == 'incorrect':
                self.feedbackSmiley = self.incorrectSmiley
            elif status == 'neutral':
                self.feedbackSmiley = self.neutralSmiley
            elif status == 'off':
                self.feedbackSmiley = self.offSmiley
        self.parent().repaint()

    def paintEvent(self, event=None):
        if self.responseLightType == self.tr("Light"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
        elif self.responseLightType == self.tr("Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Light & Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), int(self.width()+self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), int(self.width()+self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)

            
def main():
    
    prm = {}
    prm['appData'] = {}
    # create the GUI application
    qApp = QApplication(sys.argv)
    sys.excepthook = excepthook

    # prm['calledWithWAVFiles'] = False
    # parser = argparse.ArgumentParser()
    
    # parser.add_argument("-f", "--file", help="Load WAV file", nargs='*', default='')
    # args = parser.parse_args()
    # if len(args.file) > 0:
    #     prm['calledWithWAVFiles'] = True
    #     prm['WAVFilesToLoad'] = args.file

    if getattr(sys, "frozen", False):
         # The application is frozen
         prm['rootDirectory'] = os.path.dirname(sys.executable)
    else:
        prm['rootDirectory'] = os.path.dirname(__file__)

    prm = get_prefs(prm)
    prm = global_parameters(prm)
 
    #first read the locale settings
    locale = QtCore.QLocale().system().name() #returns a string such as en_US
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale, ":/translations/"):
        qApp.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("sound_source_id_" + locale, ":/translations/"):
        qApp.installTranslator(appTranslator)
    prm['appData']['currentLocale'] = QtCore.QLocale(locale)
    QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
    
    
    #then load the preferred language
    if prm['pref']['country'] != "System Settings":
        locale =  prm['pref']['language']  + '_' + prm['pref']['country']
        qtTranslator = QtCore.QTranslator()
        if qtTranslator.load("qt_" + locale, ":/translations/"):
            qApp.installTranslator(qtTranslator)
        appTranslator = QtCore.QTranslator()
        if appTranslator.load("sound_source_id_" + locale, ":/translations/") or locale == "en_US":
            qApp.installTranslator(appTranslator)
            prm['appData']['currentLocale'] = QtCore.QLocale(locale)
            QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
            prm['appData']['currentLocale'].setNumberOptions(prm['appData']['currentLocale'].NumberOption.OmitGroupSeparator | prm['appData']['currentLocale'].NumberOption.RejectGroupSeparator)

            
    qApp.setWindowIcon(QIcon(":/point-right"))
    ## Look and feel changed to CleanLooks
    #QApplication.setStyle(QStyleFactory.create("QtCurve"))
    #QApplication.setPalette(QApplication.style().standardPalette())
    #qApp.currentLocale = locale
    # instantiate the ApplicationWindow widget
    qApp.currentLocale = locale
    qApp.setApplicationName('sound_source_id')
    if platform.system() == "Windows":
        qApp.setStyle('Fusion')
    aw = applicationWindow(prm)


    # show the widget
    #aw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(qApp.exec())
if __name__ == "__main__":
    main()
   
