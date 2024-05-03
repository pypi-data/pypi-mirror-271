# -*- coding: utf-8 -*-

#   Copyright (C) 2022-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of emid

#    emid is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    emid is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.


import os, sys, platform, pickle, hashlib, base64

from .pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QFont
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont


from .utils_redirect_stream_to_file import*

if platform.system() == "Linux":
    try:
        import alsaaudio
        alsaaudioAvailable = True
    except ImportError:
        alsaaudioAvailable = False
        pass
else:
    alsaaudioAvailable = False


try:
    import pyaudio
    pyaudioAvailable = True
except ImportError:
    pyaudioAvailable = False
    pass


def set_global_parameters(prm):

    prm['backupDirectoryName'] = os.path.expanduser("~") +'/.local/share/data/emid/data_backup/'
    if os.path.exists(prm['backupDirectoryName']) == False:
        os.makedirs(prm['backupDirectoryName'])

    prm['appData']['alsaaudioAvailable'] = alsaaudioAvailable
    prm['appData']['pyaudioAvailable'] = pyaudioAvailable

    if platform.system() == 'Linux':
        prm['appData']['available_play_commands'] = []
        if os.system("which aplay") == 0:
            prm['appData']['available_play_commands'].append("aplay")
        if os.system("which play") == 0:
            prm['appData']['available_play_commands'].append("play")
        if os.system("which sndfile-play") == 0:
            prm['appData']['available_play_commands'].append("sndfile-play")
    elif platform.system() == 'Windows':
        prm['appData']['available_play_commands'] = ["winsound"]
        if os.system("where sndfile-play") == 0:
            prm['appData']['available_play_commands'].append("sndfile-play")
    elif platform.system() == 'Darwin': #that should be the MAC
        prm['appData']['available_play_commands'] = ["afplay"]
    elif platform.system() == 'FreeBSD':
        prm['appData']['available_play_commands'] = ["wavplay"]
    if alsaaudioAvailable == True:
        prm['appData']['available_play_commands'].append("alsaaudio")
    if pyaudioAvailable == True:
        prm['appData']['available_play_commands'].append("pyaudio")
    prm['appData']['available_play_commands'].append(QApplication.translate("","custom",""))

    prm['appData']['wavmanagers'] = ["wavpy", "soundfile"]

    prm['appData']['available_languages'] = ["System Settings",
                                             "en",
                                             "it",
                                             "fr",
                                             "es",
                                             "el"]
    prm['appData']['available_countries'] = {}
    prm['appData']['available_countries']['System Settings'] = ["System Settings"]
    prm['appData']['available_countries']['en'] = ["US",
                                                   "GB"]

    prm['appData']['available_countries']['it'] = ["IT",
                                                   "CH"]
    prm['appData']['available_countries']['fr'] = ["FR",
                                                   "CA"]

    prm['appData']['available_countries']['es'] = ["ES",
                                                   "BO",
                                                   "CL"]

    prm['appData']['available_countries']['el'] = ["GR",
                                                   "CY"]

  
    return prm


def def_pref(prm):

    prm["pref"] = {}
    prm["pref"]["general"] = {}
    #prm["pref"]["transducers"] = {}
    prm["pref"]["sound"] = {}
    prm["pref"]["exp"] = {}
    prm["pref"]["appearance"] = {}
    prm["appData"] = {}
    #prm["pref"]["general"]["preTrialSilence"] = "200"

    # prm["pref"]["general"]["startupCommand"] = ""
    # prm["pref"]["general"]["showBlockProgBar"] = True
    prm["pref"]["general"]["csvSeparator"] = ";"
    prm["pref"]["general"]["precision"] = 12
    prm["pref"]["general"]["responseLightDuration"] = 1000
    # # 'variable'

    # #Appearance
    # #prm["pref"]["appearance"]["style"] = QApplication.translate("","Default","")
    
    # #Sound preferences
    # #prm["pref"]["sound"]["defaultNBits"] = "32"
    # prm["pref"]["sound"]["defaultSampleRate"] = "48000"
    # prm["pref"]["sound"]["writewav"] = True
    # ##prm["pref"]["sound"]["writeSndSeqSegments"] = False
    # prm["pref"]["sound"]["writeParticipantWAVs"] = False
    prm["pref"]["sound"]["wavmanager"] = "wavpy"
    prm["pref"]["sound"]["bufferSize"] = 1024
    prm["pref"]["sound"]["appendSilence"] = 0
    prm["pref"]["sound"]["transducers"] = "Headphones 1"
    
    if platform.system() == 'Windows':
        prm["pref"]["sound"]["playCommand"] = "winsound"
        prm["pref"]["sound"]["playCommandType"] = "winsound"
    elif platform.system() == 'Darwin':
        prm["pref"]["sound"]["playCommand"] = "afplay"
        prm["pref"]["sound"]["playCommandType"] = QApplication.translate("","custom","")
    else:
        prm["pref"]["sound"]["playCommand"] = "aplay"
        prm["pref"]["sound"]["playCommandType"] = QApplication.translate("","custom","")
    if alsaaudioAvailable == True:
        prm["pref"]["sound"]["alsaaudioDevice"] = "default"
    if pyaudioAvailable == True:
        prm["pref"]["sound"]["pyaudioDevice"] = 0

    prm["pref"]["appearance"]["correctLightColor"] = (0,255,0)
    prm["pref"]["appearance"]["incorrectLightColor"] = (255,0,0)
    prm["pref"]["appearance"]["neutralLightColor"] = (255,255,255)
    prm["pref"]["appearance"]["offLightColor"] = (0,0,0)
    prm["pref"]["appearance"]["responseLightFont"] = QFont('Sans Serif', 30, QFont.Weight.Bold, False).toString()

    prm["pref"]["appearance"]["correctTextFeedback"] = "CORRECT" #QApplication.translate("","Yes","") #self.tr("CORRECT")
    prm["pref"]["appearance"]["incorrectTextFeedback"] = "INCORRECT"
    prm["pref"]["appearance"]["neutralTextFeedback"] = "DONE"
    prm["pref"]["appearance"]["offTextFeedback"] = ""
    prm["pref"]["appearance"]["correctTextColor"] = (255,255,255)
    prm["pref"]["appearance"]["incorrectTextColor"] = (255,255,255)
    prm["pref"]["appearance"]["neutralTextColor"] = (255,255,255)
    prm["pref"]["appearance"]["offTextColor"] = (255,255,255)


    # #TRANSDUCERS
    prm["transducers"] = {}
    prm["transducers"]["transducersChoices"] = ["Hadphones 1", "Speakers 1"]
    prm["transducers"]["transducersMaxLevel"] = [100, 100]
    prm["transducers"]["transducersID"] = ['0', '1']

    prm['pref']['language'] = 'System Settings'
    prm['pref']['country'] = 'System Settings'
    ##prm['pref']['randomize'] = True
    prm['pref']['startDelay'] = "500"

    return prm



def get_prefs(prm):
    prm = def_pref(prm)
    prm['prefFile'] = os.path.expanduser("~") +'/.config/emid/preferences.py'
    prm['transducersPrefFile'] = os.path.expanduser("~") +'/.config/emid/transducers.py'
    prm['experimenterPrefFile'] = os.path.expanduser("~") +'/.config/emid/experimenter.py'
    if os.path.exists(os.path.expanduser("~") +'/.config/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/')
    if os.path.exists(os.path.expanduser("~") +'/.config/emid/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/emid/')

    local_dir = os.path.expanduser("~") +'/.local/share/data/emid/'
    if os.path.exists(local_dir) == False:
        os.makedirs(local_dir)
    stdoutFile = os.path.expanduser("~") +'/.local/share/data/emid/emid_stdout_log.txt'
    sys.stdout = redirectStreamToFile(stdoutFile)
    #sys.stderr = redirectStreamToFile(stdoutFile)
    # if there is a preferences file stored load it
    cmdOutFileName = os.path.expanduser("~") +'/.local/share/data/emid/emid_cmdout_log.txt'
    prm['cmdOutFileHandle'] = open(cmdOutFileName, 'a')
    if os.path.exists(prm['prefFile']):
        fIn = open(prm['prefFile'], 'rb')
        prm['tmp'] = pickle.load(fIn)
        fIn.close()
        for k in prm['pref'].keys():
            if k in prm['tmp']:
                if type(prm['pref'][k]).__name__=='dict':
                    for j in prm['pref'][k].keys():
                        if j in prm['tmp'][k]:
                            prm['pref'][k][j] = prm['tmp'][k][j]
                else:
                     prm['pref'][k] = prm['tmp'][k]

    # if there are transducers settings stored, load them
    if os.path.exists(prm['transducersPrefFile']):
        fIn = open(prm['transducersPrefFile'], 'rb')
        prm['tmp'] = pickle.load(fIn)
        fIn.close()
        for k in prm['transducers'].keys():
            if k in prm['tmp']:
                prm['transducers'][k] = prm['tmp'][k]

    # if there are experimenter settings stored, load them
    if os.path.exists(prm['experimenterPrefFile']):
        fIn = open(prm['experimenterPrefFile'], 'rb')
        prm['tmp'] = pickle.load(fIn)
        fIn.close()
        for k in prm['experimenter'].keys():
            if k in prm['tmp']:
                prm['experimenter'][k] = prm['tmp'][k]
    return prm



    
