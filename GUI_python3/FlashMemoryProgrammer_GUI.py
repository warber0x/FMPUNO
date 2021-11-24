#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author of this software: Warber0x.
# @Date: 26/12/2021
# @Version: 1.0 Beta
# @Baud rate: Check the arduino Sketch

# THIS NEEDS A WXPYTHON TO BE EXECUTED.
# Systel used Kali 2020
# Python version 3

# This is the latest version that's compatible with python 3

import wx
import os
import sys
import time
import serial
import struct
import _thread
import threading
import binascii
import ctypes
import time

from wx.lib.buttons import GenBitmapTextButton
from pubsub import pub


class programmer_gui(wx.Frame):
    gauge_counter = 0
    def __init__(self, parent, id):

        wx.Frame.__init__(
            self,
            parent,
            id,
            'FMPUNO (Flash Memory Programmer UNO) - By Warber0x (github)'
                ,
            size=(900, 450),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
                ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX,
            )

        panel = wx.Panel(self, pos=(0, 100), size=(700, 200))
        self.percent = 0

        img = wx.Image('./avr.png')
        img.Rescale(170, 170)
        png = wx.Bitmap(img)
        wx.StaticBitmap(panel, -1, png, (713, 170), (png.GetWidth(),
                        png.GetHeight()))

        # Menu Gui

        status = self.CreateStatusBar()

        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        editmenu = wx.Menu()
        aboutmenu = wx.Menu()

        exititem = filemenu.Append(wx.NewIdRef(), '&Exit', '')
        aboutitem = aboutmenu.Append(wx.NewIdRef(), '&About',' Information about this program')
        edititem1 = editmenu.Append(wx.NewIdRef(), '&Read', '')
        edititem2 = editmenu.Append(wx.NewIdRef(), '&Erase', '')
        edititem3 = editmenu.Append(wx.NewIdRef(), '&Program', '')

        menubar.Append(filemenu, 'File')
        menubar.Append(editmenu, 'Edit')
        menubar.Append(aboutmenu, '?')

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
        self.Bind(wx.EVT_MENU, self.OnExit, exititem)
        self.Bind(wx.EVT_MENU, self.OnRead, edititem1)
        self.Bind(wx.EVT_MENU, self.OnErase, edititem2)
        self.Bind(wx.EVT_MENU, self.OnProgram, edititem3)

        # End menubar

        # imageFile = "write.png"
        # imageFile2 = "read.png"
        # imageFile3 = "erase.png"
        # imageFile4 = "info.png"

        # imageWrite = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # imageRead = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # imageErase = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # imageInfo = wx.Image(imageFile4, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

        font3 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
        label6 = wx.StaticText(panel, -1, 'IC Operations:', (10, 200), size=(200, -1))
        label6.SetFont(font3)

        self.buttonProgram = wx.Button(panel, id=-1, label='Upload', pos=(50, 240), size=(65, 40))
        self.buttonRead = wx.Button(panel, id=-1, label='Read',  pos=(50 + 65, 240), size=(65, 40))
        self.buttonErase = wx.Button(panel, id=-1, label='Erase',pos=(50, 280), size=(65, 40))
        self.buttonInfo = wx.Button(panel, id=-1, label='Infos', pos=(50 + 65, 280), size=(65, 40))

        self.textarea = wx.TextCtrl(panel, pos=(240, 10), style=wx.TE_MULTILINE | wx.TE_READONLY, size=(450, 265))

        font1 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
        label1 = wx.StaticText(panel, -1, 'File to Upload', (10, 10), size=(200, -1))
        label1.SetFont(font1)

        label4 = wx.StaticText(panel, -1, 'Game File: ', (10, 40))
        self.uploadText = wx.TextCtrl(panel, -1, pos=(85, 40), size=(100, -1), style=wx.TE_READONLY)
        buttonDlg = wx.Button(panel, id=-1, label='...', pos=(185,40), size=(40, 30))

        self.ln = wx.StaticLine(panel, -1, pos=(20, 80), size=(200,-1), style=wx.LI_HORIZONTAL)

        font1 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
        label1 = wx.StaticText(panel, -1, 'Parameters:', (10, 90), size=(200, -1))
        label1.SetFont(font1)

        label3 = wx.StaticText(panel, -1, 'Baude Rate: ', (10, 120), size=(200, -1))
        baude = [
            '115200',
            '57600',
            '38400',
            '28800',
            '19200',
            '14400',
            '9600',
            '4800',
            ]
        self.baudBox = wx.ComboBox(panel,-1,pos=(100, 120),size=(100, -1),choices=baude,style=wx.CB_READONLY,)

        label5 = wx.StaticText(panel, -1, 'Serial port: ', (10, 150), size=(200, -1))
        arduinoSerial = ['ttyACM0', 'ttyACM1', 'ttyACM2', 'ttyACM3', 'ttyACM4']
        self.serialBox = wx.ComboBox(panel,-1,pos=(100, 150),size=(100, -1),choices=arduinoSerial,style=wx.CB_READONLY,)

        self.ln = wx.StaticLine(panel, -1, pos=(20, 190), size=(200, 1), style=wx.LI_HORIZONTAL)

        gaugeText = wx.StaticText(panel, -1, 'Progress %: ', (240, 283))
        self.gauge = wx.Gauge(panel, -1, 100, pos=(240, 300), size=(450, 25))

        # create a pubsub listener
        pub.subscribe(self.updateProgress, "update")

        font6 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
        label6 = wx.StaticText(panel, -1, 'IC Info', (710, 10), size=(200, -1))
        label6.SetFont(font6)

        label7 = wx.StaticText(panel, -1, 'Man ID: ', (710, 45))
        self.manid = wx.TextCtrl(panel, -1, pos=(770, 45), size=(120,
                                 -1), style=wx.TE_READONLY)

        label8 = wx.StaticText(panel, -1, 'Dev ID: ', (710, 80))
        self.devid = wx.TextCtrl(panel, -1, pos=(770, 80), size=(120,
                                 -1), style=wx.TE_READONLY)

        label2 = wx.StaticText(panel, -1, 'Brand : ', (710, 115))
        chip = ['AM29F010', 'AM29F040']
        self.flashref = wx.TextCtrl(panel, -1, pos=(770, 115), size=(120,
                                    -1), style=wx.TE_READONLY)

        self.ln = wx.StaticLine(panel, -1, pos=(700, 150), size=(200,
                                -1), style=wx.LI_HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, self.OnProgram, self.buttonProgram)
        self.Bind(wx.EVT_BUTTON, self.OnDlg, buttonDlg)
        self.Bind(wx.EVT_BUTTON, self.OnRead, self.buttonRead)
        self.Bind(wx.EVT_BUTTON, self.OnErase, self.buttonErase)
        self.Bind(wx.EVT_BUTTON, self.OnInfos, self.buttonInfo)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        self.intro = \
            '''ARDUINO AMD FLASH MEMORY PROGRAMMER - XXX29F0XX Series
            @Version: 1.0
            @Arduino ver: UNO
            @Python 3.9.1+
            @Author: https://github.com/warber0x

            Please connect your programmer, select the serial port, choose the baud rate and press one of the operations

            The programmed baudrate in this version is 115200 (Recommended)

            '''
        self.intro = self.intro.upper()
        self.textarea.SetValue(self.intro)

        self.count = 0

# # # # # # # # # # # # # # # # # # # # # # # # 

    def file_size_mb(filePath):
        return os.path.getsize(filePath)

# # # # # # # # # # # # # # # # # # # # # # # # # 

    def setButtonDisable(self):
        self.buttonProgram.Disable()
        self.buttonRead.Disable()
        self.buttonInfo.Disable()
        self.buttonErase.Disable()

# # # # # # # # # # # # # # # # # # # # # # # # # 

    def setButtonEnable(self):
        self.buttonProgram.Enable()
        self.buttonRead.Enable()
        self.buttonInfo.Enable()
        self.buttonErase.Enable()

# # # # # # # # # # # # # # # # # # # # # # # # # 

    def setStatusText(self, string):
        self.SetStatusText(string)

# # # # # # # # # # # # # # # # # # # # # # # # # 

    def OnDlg(self, event):
        dlg = wx.FileDialog(
            self,
            'Choose a file',
            os.getcwd(),
            '',
            '*.*',
            wx.FD_OPEN,
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            mypath = os.path.basename(path)
            self.uploadText.SetValue(path)
            self.SetStatusText('You selected: %s' % mypath)
        else:
            self.uploadText.SetValue("")
            self.SetStatusText("")

        dlg.Destroy()

# # # # # # # # # # # # # # # # # # # # # # # # 

    def OnExit(self, event):
        self.Destroy()

        # self.count += 1
        # self.gauge.SetValue(self.count)
        # self.SetStatusText(str(self.count) + "% Done")

# # # # # # # # # # # # # # # # # # # # # # # # 

    def OnAbout(self, event):

                # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.

        dlg = wx.MessageDialog(self,
                               ''' AMD Flash Memory Programmer.
                                Ver 0.1
                                Copyright 2013 - Warber0x (github).''',
                               ' AMD Flash Programmer', wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

# # # # # # # # # # # # # # # # # # # # # # # # 

    def OnRead(self, event):

        self.gauge.SetValue(0)
        self.gauge_counter = 0
        t1 = GaugeThread()

        self.percent = 0
        port = '/dev/' + str(self.serialBox.GetValue())
        baudrate = str(self.baudBox.GetValue())

        # serial = 0

        car = ''
        self.textarea.SetValue(self.intro)

        if str(self.serialBox.GetValue()) != '' and baudrate != '':
            line = 1
            temp_intro = self.textarea.GetValue()
            count = 0
            counter = 0
            val = ''
            total = 0x1FF / 100  # 0x1FF in arduino code
            i = 0
            linecount = 0

            try:
                arduino = serial.Serial(port, int(float(baudrate)),
                        timeout=1)
            except:
                dlg = wx.MessageDialog(self,
                        "Can't communicate with Arduino, please check serial ports !!!"
                        , 'Communication Problem', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            time.sleep(2)

            self.SetStatusText('Please wait ...')

            car = car + str("%02d" % linecount) + '\t\t'
            car = car.upper()

            command = 'R'
            arduino.write(command.encode())

            time.sleep(.001)                    # delay of 1ms
            val = arduino.readline()                # read complete line from serial output
            self.SetStatusText('Reading the memory chip ...')
            while not '\\n'in str(val):  
                time.sleep(.001)                # delay of 1ms 
                temp = arduino.readline()           # check for serial output.
                if not not temp.decode():       # if temp is not empty.
                    val = (val.decode()+temp.decode()).encode()
                    # requrired to decode, sum, then encode because
                    # long values might require multiple passes
            val = val.decode()                  # decoding from bytes
            val = val.strip()                   # stripping leading and trailing spaces.
            
            
            for value in str(val):
                car = car + value
                count += 1
                if count == 2:
                    car = car + ' '
                    count = 0

                if line != 32:
                    line += 1
                else:
                    car = car + '\n'
                    line = 1
                    linecount += 1
                    car = car + str("%02d" % linecount) + '\t\t'
                    car = car.upper()
                
                self.percent = round(i / total)
                i += 1

            car += '\n\n' + str(temp_intro)
            car = car.upper()

            '''while 1:
                # val = arduino.read()

                if str(val) in '\\n': 
                   break

                car = car + val

                count += 1

                if count == 2:

                    # self.textarea.SetValue(" "),

                    car = car + ' '
                    count = 0

                if line != 32:
                    line += 1
                else:
                    car = car + '\n'
                    line = 1
                    linecount += 1
                    car = car + str(struct.pack('>I',linecount)) + '          '
                    car = car.upper()

                self.percent = round(i / total)
                i += 1'''

            
            self.textarea.SetValue(car)
            self.SetStatusText('Operation Completed Successfully.')
            dlg = wx.MessageDialog(self, 'Operation Completed', 'IC read', wx.OK)
            arduino.close()
        else:

            dlg = wx.MessageDialog(self,
                                   "Can't communicate with Arduino, please check the fileds"
                                   , 'Incorrect values', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

            # self.textarea.SetValue(car)
        t1.raise_exception()
        t1.join()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def OnErase(self, event):
        counter = 0
        port = '/dev/' + str(self.serialBox.GetValue())
        baudrate = str(self.baudBox.GetValue())

        if str(self.serialBox.GetValue()) != '' and baudrate != '':

            # self.textarea.SetValue('')

            port = '/dev/' + str(self.serialBox.GetValue())
            baudrate = str(self.baudBox.GetValue())

            # serial = 0

            percent = 0

            try:
                arduino = serial.Serial(port, int(float(baudrate)),
                        timeout=1)
            except:
                dlg = wx.MessageDialog(self,
                        "Can't communicate with Arduino, please check serial ports"
                        , 'Communication Problem', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            time.sleep(2)

            self.SetStatusText('Erasing, Please wait ...')

            command = "E"
            arduino.write(command.encode())
            response = ''
            time.sleep(.001)                    # delay of 1ms
            val = arduino.readline()                # read complete line from serial output
        
            while not '\\n'in str(val):  
                time.sleep(.001)                # delay of 1ms 
                temp = arduino.readline()           # check for serial output.
                if not not temp.decode():       # if temp is not empty.
                    val = (val.decode()+temp.decode()).encode()
                    # requrired to decode, sum, then encode because
                    # long values might require multiple passes
            val = val.decode()                  # decoding from bytes
            val = val.strip()                   # stripping leading and trailing spaces.

            response = val
            self.SetStatusText('Operation Completed Successfully.')
            dlg = wx.MessageDialog(self, 'Flash memory %s' % response, 'IC Erase', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

            arduino.close()
            
        else:
            dlg = wx.MessageDialog(self, "Can't communicate with Arduino, please check the fields" , 'Incorrect values', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def OnProgram(self, event):

                # #######################################################################
                # The following functions are destined to program the memory chip
                # Should be included in function to be organizedreflexion
                # Mind the logic of the algorithm
                # #######################################################################

        gameSize = 0
        game = ''

                # Open Serial port and wait arduino to reset

        port = '/dev/' + str(self.serialBox.GetValue())
        baudrate = str(self.baudBox.GetValue())

        try:
            arduino = serial.Serial(port, int(float(baudrate)),
                                    timeout=1)
        except:
            dlg = wx.MessageDialog(self,
                                   "Can't communicate with Arduino, please check serial ports", 'Communication Problem', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return

        self.SetStatusText('Please wait ...')
        time.sleep(2)

        # Get Game size and send it to Arduino

        path = self.uploadText.GetValue()

        if path != '':
            self.SetStatusText('Getting file path ...')
            gameSize = os.path.getsize(path)

            # Send begin command to Arduino and
            # Wait OK from Arduino to begin programming
            # Set Arduino in programming mode and wait for its response

            command = 'W'
            arduino.write(command.encode())

            val = arduino.read()                # read complete line from serial output
            if '+' in str(val):
                self.SetStatusText('Uploading ... ')
            else:
                self.SetStatusText('Error Uploading ...')
                return

            arduino.write(str(gameSize).encode())

            val = arduino.read()                # read complete line from serial output
            if '+' in str(val):
                self.SetStatusText('Uploading ... Please wait')
                game = open(self.uploadText.GetValue(), 'rb')
                total = gameSize / 100
                percent = 0
            else:
                self.SetStatusText('Error Uploading ... Maybe the Arduino')
                return

            # progressFrame = progressBar(parent = None, id = -1)
            # progressFrame.Show()
            # thread.start_new_thread(self.OnNewUpdate, (gameSize, game, total, arduino,self,))

            self.OnNewUpdate(gameSize, game, total, arduino, self)
        else:
            dlg = wx.MessageDialog(self, 'Gameboy ROM file is missing', 'ROM File', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def OnInfos(self, event):

        # Get Device ID - First
        # Get Manufacturer ID - Second

        # Start Device ID Operation
        #
        self.gauge_counter = 0
        t1 = GaugeThread()

        car = ''
        count = ''
        counter = 0
        baudrate = 0
        port = ''

        man = ''
        ref = ''

        self.gauge.SetValue(0)
        self.devid.SetValue('')
        self.manid.SetValue('')
        self.flashref.SetValue('')

        if str(self.serialBox.GetValue()) != '' and baudrate != '':
            self.SetStatusText('Please wait ... ')

            self.percent = 0
            port = '/dev/' + str(self.serialBox.GetValue())
            baudrate = str(self.baudBox.GetValue())

            percent = 0

            try:
                arduino = serial.Serial(port, int(float(baudrate)),
                        timeout=1)
            except:
                dlg = wx.MessageDialog(self,
                        "Can't communicate with Arduino, please check serial ports"
                        , 'Communication Problem', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return

            time.sleep(2)

            response1 = '0x'
            response2 = '0x'

            command = "D"
            arduino.write(command.encode())

            time.sleep(.001)                    # delay of 1ms
            val = arduino.readline()                # read complete line from serial output
            self.SetStatusText('Getting Device ID ...')
            while not '\\n'in str(val):  
                time.sleep(.001)                # delay of 1ms 
                temp = arduino.readline()           # check for serial output.
                if not not temp.decode():       # if temp is not empty.
                    val = (val.decode()+temp.decode()).encode()
                    # requrired to decode, sum, then encode because
                    # long values might require multiple passes
            val = val.decode()                  # decoding from bytes
            val = val.strip()                   # stripping leading and trailing spaces.
            response1 = response1 + val
            ref = ref + val

            # Just to complete the DevID field#

            if ref == '0':
                response1 += '0'

            # self.devid.SetValue(response1)
            arduino.close()

            # Get Manufacturer - Start second operation
            ## # # # # # # # # # # # # # # # # # # # # # # # 
            car = ''
            count = ''
            counter = 0
            baudrate = 0
            port = ''

            if str(self.serialBox.GetValue()) != '' and baudrate != '':
                self.SetStatusText('Please wait ...')

                self.percent = 0
                port = '/dev/' + str(self.serialBox.GetValue())
                baudrate = str(self.baudBox.GetValue())

                percent = 0
                arduino = serial.Serial(port, int(float(baudrate)),
                        timeout=1)
                time.sleep(2)

                response2 = '0x'

                command = "I"
                arduino.write(command.encode())

                time.sleep(.001)                    # delay of 1ms
                val = arduino.readline()                # read complete line from serial output
                self.SetStatusText('Getting Manufacturer ID...')
                while not '\\n' in str(val):  
                    time.sleep(.001)                # delay of 1ms 
                    temp = arduino.readline()           # check for serial output.
                    if not not temp.decode():       # if temp is not empty.
                        val = (val.decode()+temp.decode()).encode()
                        # requrired to decode, sum, then encode because
                        # long values might require multiple passes
                val = val.decode()                  # decoding from bytes
                val = val.strip()                   # stripping leading and trailing spaces.
                response2 = response2 + val
                man = man + val
                
                self.devid.SetValue(response1)
                self.manid.SetValue(response2)

                if man == '01':
                    self.flashref.SetValue('AMD ')
                if man == '37':
                    self.flashref.SetValue('AMIC ')
                if man != '37' and man != '01':
                    self.flashref.SetValue('No chip found')

                if ref == '20':
                    self.flashref.SetValue(self.flashref.GetValue()
                            + 'AM29F010B')
                if ref == 'A4':
                    self.flashref.SetValue(self.flashref.GetValue()
                            + 'AM29F040B')
                if ref == '86':
                    self.flashref.SetValue(self.flashref.GetValue()
                            + 'A29040B')

                self.SetStatusText('Operation Completed Successfully.')
                arduino.close()
        else:

            dlg = wx.MessageDialog(self, 'Please check the fields', 'Incorrect values', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

        t1.raise_exception()
        t1.join()

    # Code recently added this code is for a new progress bar
    # The old one had bugs sometimes, so I have to change its code

    def OnNewUpdate(
        self,
        gameSize,
        gamepath,
        total,
        arduinoport,
        mainFrame,
        ):
        pulse_dlg = wx.ProgressDialog(title='Upload Command', message='Uploading, Keep arduino connected ...', maximum=gameSize)

          # Some stuff happens
          # self.progressBar.SetRange(gameSize)

        mainFrame.setButtonDisable()
        car = ''

        for x in range(0, gameSize):
            car = gamepath.read(1)
            arduinoport.write(car)

              # time.sleep(0.006)
              # self.progressBar.SetValue(x)
              # self.Refresh()
              # wx.MilliSleep(1)

            pulse_dlg.Update(x)

          # self.SetStatusText("Uploading is almost finished ... ")
          # time.sleep(2)

        self.SetStatusText('Upload completed.')

        mainFrame.setButtonEnable()
        arduinoport.close()
        gamepath.close()
        pulse_dlg.Destroy()

        dlg = wx.MessageDialog(self, 'Upload completed', 'IC writing', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def updateProgress(self, msg):
        self.gauge_counter += 50
        
        self.gauge.SetValue(self.gauge_counter)
        self.gauge.Refresh()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class progressBar(wx.Frame):

    def __init__(self, parent, id):
        self.window = wx.Frame.__init__(
            self,
            parent,
            id,
            'ProgressBar',
            size=(360, 90),
            style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
                ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX,
            )
        status = self.CreateStatusBar()
        panel = wx.Panel(self, pos=(0, 0), size=(100, 300))
        self.progressBar = wx.Gauge(panel, -1, 0, pos=(30, 20),
                                    size=(300, 30))
        self.SetStatusText('Uploading is in progress, Please wait ')
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def update(
        self,
        gameSize,
        gamepath,
        total,
        arduinoport,
        mainFrame,
        ):
        self.progressBar.SetRange(gameSize)
        mainFrame.setButtonDisable()
        car = ''

        for x in range(0, gameSize):
            car = gamepath.read(1)
            arduinoport.write(car)

                        # time.sleep(0.006)

            self.progressBar.SetValue(x)
            self.Refresh()

        self.SetStatusText('Uploading is almost finished ... ')
        time.sleep(2)
        self.SetStatusText('Uploading complete.')

        mainFrame.setButtonEnable()
        arduinoport.close()
        gamepath.close()
        self.Destroy()
        return

    def OnClose(self, evt):
        return

# # # # # # # # # # # # # # # # # # # # # # # # # # 

class GaugeThread(threading.Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.start()    # start the thread
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(2):
            wx.CallAfter(pub.sendMessage, "update", msg="update")


    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

# # # # # # # # # # # # # # # # # # # # # # # # # # 

class OperationsThread(threading.Thread):
 
    def __init__(self, target, *args):
        self._target = target
        threading.Thread.__init__(self)

    def run(self):
        self._target()

# # # # # # # # # # # # # # # # # # # # # # # # # # 

class starter(threading.Thread):

    def __init__(
        self,
        threadID,
        name,
        counter,
        ):
        threading.Thread.__init__(self)
        frame = programmer_gui(parent=None, id=-1)
        frame.Show()

    def run(self):
        pass


if __name__ == '__main__':
    app = wx.App(False)

    # Create new threads

    thread1 = starter(1, 'Thread-1', 1)
    # Start new Threads

    thread1.start()
    app.MainLoop()
