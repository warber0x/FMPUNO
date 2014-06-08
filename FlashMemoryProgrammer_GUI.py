#!/usr/bin/python

#THIS NEEDS A WXPYTHON TO BE EXECUTED.

import wx
import os, sys
import time
import serial
import struct
import thread
import threading

from wx.lib.buttons import GenBitmapTextButton

class programmer_gui(wx.Frame): 
        def __init__(self, parent, id):
                
                wx.Frame.__init__(self, parent, id, 'AMD Programmer - By Warber0x (Radouane SAMIR)', size = (900, 380), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX)
                
                panel = wx.Panel(self, pos = (0, 100), size = (700, 200))
                self.percent = 0
                
                #png = wx.Image('/root/Desktop/Flash_EEPROM_Programmer_soft/Programmer V1.2/arduino2.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                #wx.StaticBitmap(panel, -1, png, (723, 221), (png.GetWidth(), png.GetHeight()))
                
                #Menu Gui
                status = self.CreateStatusBar()
                
                menubar = wx.MenuBar()
                filemenu = wx.Menu()
                editmenu = wx.Menu()
                aboutmenu = wx.Menu()
                

                exititem = filemenu.Append(wx.NewId(), "&Exit", "")
                aboutitem = aboutmenu.Append(wx.NewId(), "&About"," Information about this program")
                edititem1 = editmenu.Append(wx.NewId(), "&Read", "")
                edititem2 = editmenu.Append(wx.NewId(), "&Erase", "")
                edititem3 = editmenu.Append(wx.NewId(), "&Program", "")
                
                menubar.Append(filemenu, "File")
                menubar.Append(editmenu, "Edit")
                menubar.Append(aboutmenu, "?")
                
                self.SetMenuBar(menubar)
                self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
                self.Bind(wx.EVT_MENU, self.OnExit,  exititem)
                self.Bind(wx.EVT_MENU, self.OnRead,  edititem1)
                self.Bind(wx.EVT_MENU, self.OnErase,  edititem2)
                self.Bind(wx.EVT_MENU, self.OnProgram,  edititem3)
                
                #End menubar
                
                #imageFile = "write.png"
                #imageFile2 = "read.png"
                #imageFile3 = "erase.png"
                #imageFile4 = "info.png"
                
                #imageWrite = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                #imageRead = wx.Image(imageFile2, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                #imageErase = wx.Image(imageFile3, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                #imageInfo = wx.Image(imageFile4, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
                
                font3 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
                label6 = wx.StaticText(panel, -1, "Memory Operations", (20, 180))
                label6.SetFont(font3)
                
                self.buttonProgram = wx.Button(panel, id=-1,  label="Upload", pos = (50, 210), size = (65, 40))
                self.buttonRead = wx.Button(panel, id=-1, label="Read",  pos = (50+70, 210), size = (65, 40))
                self.buttonErase = wx.Button(panel, id=-1,  label="Erase",pos = (50, 250), size = (65, 40))
                self.buttonInfo = wx.Button(panel, id=-1, label="Infos", pos = (50+70, 250), size = (65, 40))
                
                self.textarea = wx.TextCtrl(panel, pos=(240, 10), style=wx.TE_MULTILINE | wx.TE_READONLY, size=(450,265))
                
                
                font1 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
                label1 = wx.StaticText(panel, -1, "Programmer Setup", (30, 10))
                label1.SetFont(font1)
                
                label2 = wx.StaticText(panel, -1, "Flash Ref.: ", (10, 47))
                chip = ['AM29F010', 'AM29F040']
                self.flashref = wx.TextCtrl(panel, -1, pos=(85, 40), size=(100, -1), style=wx.TE_READONLY)
                
                label3 = wx.StaticText(panel, -1, "Baude Rate: ", (10, 78))
                baude = ['115200', '57600', '38400', '28800', '19200', '14400', '9600', '4800']
                self.baudBox = wx.ComboBox(panel, -1, pos=(85, 73), size=(100, -1), choices=baude, style=wx.CB_READONLY)
                
                label4 = wx.StaticText(panel, -1, "Game File: ", (10, 110))
                self.uploadText = wx.TextCtrl(panel, -1, pos=(85, 105), size=(100, -1), style = wx.TE_READONLY)
                buttonDlg = wx.Button(panel, id=-1, label='...', pos = (185, 105), size = (40,25))
                
                label5 = wx.StaticText(panel, -1, "Serial port: ", (10, 140))
                arduinoSerial = ['ttyACM0', 'ttyACM1', 'ttyACM2', 'ttyACM3','ttyACM4']
                self.serialBox = wx.ComboBox(panel, -1, pos=(85, 135), size=(100, -1), choices=arduinoSerial, style=wx.CB_READONLY)
                
                self.ln = wx.StaticLine(panel, -1, pos=(20, 170), size=(200, -1), style=wx.LI_HORIZONTAL)
                
                gaugeText= wx.StaticText(panel, -1, "Transfer status: ", (240, 283))
                self.gauge = wx.Gauge(panel, -1, 100, pos=(240, 300), size=(450, 25))
                
                
                font6 = wx.Font(12, wx.NORMAL, wx.ITALIC, wx.BOLD)
                label6 = wx.StaticText(panel, -1, "Memory infos", (730, 10))
                label6.SetFont(font6)
                
                label7 = wx.StaticText(panel, -1, "Man ID: ", (710, 45))
                self.manid = wx.TextCtrl(panel, -1, pos=(770, 40), size=(120, -1), style = wx.TE_READONLY)
                
                label8 = wx.StaticText(panel, -1, "Dev ID: ", (710, 70))
                self.devid = wx.TextCtrl(panel, -1, pos=(770, 70), size=(120, -1), style = wx.TE_READONLY)
                
                self.ln = wx.StaticLine(panel, -1, pos=(700, 110), size=(200, -1), style=wx.LI_HORIZONTAL)
            
                self.Bind(wx.EVT_BUTTON, self.OnProgram, self.buttonProgram)
                self.Bind(wx.EVT_BUTTON, self.OnDlg, buttonDlg)
                self.Bind(wx.EVT_BUTTON, self.OnRead, self.buttonRead)
                self.Bind(wx.EVT_BUTTON, self.OnErase, self.buttonErase)
                self.Bind(wx.EVT_BUTTON, self.OnInfos, self.buttonInfo)
                self.Bind(wx.EVT_CLOSE, self.OnExit)    
                
                self.intro = 'ARDUINO AMD FLASH MEMORY PROGRAMMER - XXX29F0XX Series\n@Version: 1.0\n@Arduino ver: UNO\n@Author: Radouane SAMIR - SamCreation 2013\n\nPlease connect your programmer, select the serial port, choose the baud rate and press one of the operations\n\n'
                self.intro = self.intro.upper()
                self.textarea.SetValue(self.intro);
                
                self.count = 0
                
        def file_size_mb(filePath): 
                return os.path.getsize(filePath)
                
        def setButtonDisable(self):
                self.buttonProgram.Disable()
                self.buttonRead.Disable()
                self.buttonInfo.Disable()
                self.buttonErase.Disable()
        
        def setButtonEnable(self):
                self.buttonProgram.Enable()
                self.buttonRead.Enable()
                self.buttonInfo.Enable()
                self.buttonErase.Enable()
                
        def setStatusText(self, string):
                self.SetStatusText(string)
                
        def OnDlg(self, event):
                dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
                if dlg.ShowModal() == wx.ID_OK:
                        path = dlg.GetPath()
                        mypath = os.path.basename(path)
                        self.uploadText.SetValue(path)
                        self.SetStatusText("You selected: %s" % mypath)
                dlg.Destroy()           
                
        def OnExit(self, event):
                self.Destroy()
                #self.count += 1
                #self.gauge.SetValue(self.count)
                #self.SetStatusText(str(self.count) + "% Done")
                
        def OnAbout(self,event):
                # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
                dlg = wx.MessageDialog( self, " AMD Flash Memory Programmer.\n Ver 0.1\n Copyright 2013 - Radouane SAMIR.", " AMD Flash Programmer", wx.OK)
                dlg.ShowModal() # Show it
                dlg.Destroy() # finally destroy it when finished.
        
        def OnRead(self, event):
        
                self.gauge.SetValue(0)
                
                self.percent = 0
                port = "/dev/" + str(self.serialBox.GetValue())
                baudrate = str(self.baudBox.GetValue())
                
                #serial = 0
                
                car = ''
                self.textarea.SetValue(self.intro)
                
                if (str(self.serialBox.GetValue()) != '' and baudrate != ''):
                        self.SetStatusText("Please wait ...")
                        
                        line = 1
                        car = self.textarea.GetValue()
                        count = 0
                        counter = 0
                        val = ''
                        total = 0x1FF / 100 #0x1FF in arduino code
                        i = 0
                        linecount = 0
                        
                        arduino = serial.Serial(port, int(baudrate), timeout = 1)
                        time.sleep(2)
                        
                        car = car + str(struct.pack(">I", linecount).encode('hex')) + "          "
                        car = car.upper()
                        
                        arduino.write("R")
                        while(1):
                                val = arduino.read()
                                car = car + val 
                                
                                count += 1
                
                                if (count==2):
                                        #self.textarea.SetValue(" "),
                                        car = car + " "
                                        count = 0
                        
                                if (line != 32):
                                        line += 1
                                else:
                                        car = car + '\n'
                                        line = 1
                                        linecount += 1
                                        car = car + str(struct.pack(">I", linecount).encode('hex')) + "          "
                                        car = car.upper()
                                        
                                if (val == '\n'):
                                        break
                                        
                                self.percent = round(i / total)
                                i += 1
                                        
                        arduino.close()
                        
                        while (counter <= 99):
                                counter += 1
                                self.gauge.SetValue(counter)
                                self.SetStatusText(str(counter) + "% Done")
                        
                        self.textarea.SetValue(car)
                        
                else:
                        dlg = wx.MessageDialog(self, "Please check the value selected", "Incorrect values", wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                        #self.textarea.SetValue(car)
        
        def OnErase(self, event):
                counter = 0
                port = "/dev/" + str(self.serialBox.GetValue())
                baudrate = str(self.baudBox.GetValue())
                
                if (str(self.serialBox.GetValue()) != '' and baudrate != ''):
                        self.SetStatusText("Please wait ...")
                        
                        #self.textarea.SetValue('')
                        port = "/dev/" + str(self.serialBox.GetValue())
                        baudrate = str(self.baudBox.GetValue())
                        #serial = 0
        
                        percent = 0
                        arduino = serial.Serial(port, int(baudrate), timeout = 1)
                        time.sleep(2)
        
                        arduino.write("E")
                        response = ''
                        while(1):
                                car = arduino.read()
                                response += car
                                if (car == '\n'):
                                        break
                                
                        while (counter <= 99):
                                counter += 1
                                self.gauge.SetValue(counter)
                                self.SetStatusText(str(counter) + "% Done")
        
                        dlg = wx.MessageDialog(self, "Flash memory %s" %response, "Erasure Operation", wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
        
                        arduino.close()
                else:
                        dlg = wx.MessageDialog(self, "Please check the value selected", "Incorrect values", wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                        
        
        def OnProgram(self, event):
                ########################################################################
                # The following functions are destined to program the memory chip
                # Should be included in function to be organizedreflexion
                # Mind the logic of the algorithm
                ########################################################################

                gameSize = 0
                
                #Open Serial port and wait arduino to reset
                port = "/dev/" + str(self.serialBox.GetValue())
                baudrate = str(self.baudBox.GetValue())
                arduino = serial.Serial(port, int(baudrate), timeout = 1)
                time.sleep(2)

                #Get Game size and send it to Arduino
                path = self.uploadText.GetValue()
                gameSize = os.path.getsize(path)

                #Send begin command to Arduino and
                #Wait OK from Arduino to begin programming
                #Set Arduino in programming mode and wait for its response

                arduino.write('W')
                while (arduino.read() != '+'):
                        pass

                arduino.write(str(gameSize))    
        
                while (arduino.read() != '+'):
                        pass

                game = open(self.uploadText.GetValue(), 'r')

                total = gameSize / 100
                percent = 0
                
                progressFrame = progressBar(parent = None, id = -1)
                progressFrame.Show()
                thread.start_new_thread(progressFrame.update, (gameSize, game, total, arduino,self,))
        
        def OnInfos(self, event):
                #Get Device ID - First
                #Get Manufacturer ID - Second
                
                #Start Device ID Operation
                self.gauge.SetValue(0)
                
                car = ''
                count = ''
                counter = 0
                baudrate = 0
                port = ''
                
                man = ''
                ref =''
                
                self.gauge.SetValue(0)
                self.devid.SetValue("")
                self.manid.SetValue("")
                
                if (str(self.serialBox.GetValue()) != '' and baudrate != ''):
                        self.SetStatusText("Please wait ...")
                        
                        self.percent = 0
                        port = "/dev/" + str(self.serialBox.GetValue())
                        baudrate = str(self.baudBox.GetValue())
                
                        percent = 0
                        arduino = serial.Serial(port, int(baudrate), timeout = 1)
                        time.sleep(2)
                        
                        response1 = '0x'
                        response2 = '0x'
                
                        arduino.write("D")
                        while (1):
                                car = arduino.read()
                                if (car == '\n' or car == '\r'):
                                        break
                        
                                if (car != '\n' and car != '\r'):
                                        response1 += car
                                        ref += car
        
                        self.devid.SetValue(response1)
                        arduino.close() 
                        
                        #Get Manufacturer - Start second operation
                        car = ''
                        count = ''
                        counter = 0
                        baudrate = 0
                        port = ''

                
                        if (str(self.serialBox.GetValue()) != '' and baudrate != ''):
                                self.SetStatusText("Please wait ...")
                        
                                self.percent = 0
                                port = "/dev/" + str(self.serialBox.GetValue())
                                baudrate = str(self.baudBox.GetValue())
                
                                percent = 0
                                arduino = serial.Serial(port, int(baudrate), timeout = 1)
                                time.sleep(2)
                        
                                response2 = '0x'
                
                                arduino.write("I")
                                while (1):
                                        car = arduino.read()
                                        if (car == '\n' or car == '\r'):
                                                break
                        
                                        if (car != '\n' and car != '\r'):
                                                response2 += car
                                                man += car                                      
                                        
                                while (counter <= 99):
                                        counter += 1
                                        self.gauge.SetValue(counter)
                                        self.SetStatusText(str(counter) + "% Done")
        
                                self.manid.SetValue(response2)
        
                                arduino.close() 
                                
                                if (man == '01'):
                                        self.flashref.SetValue("AMD ")
                                if (man == '37'):
                                        self.flashref.SetValue("AMIC ")
                                        
                                if (ref == '20'):
                                        self.flashref.SetValue(self.flashref.GetValue() + "AM29F010B")
                                if (ref == 'A4'):
                                        self.flashref.SetValue(self.flashref.GetValue() + "AM29F040B")
                                if (ref == '86'):
                                        self.flashref.SetValue(self.flashref.GetValue() + "A29040B")
                                                
                        
                else:
                        dlg = wx.MessageDialog(self, "Please check the value selected", "Incorrect values", wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                                                
class progressBar(wx.Frame):
        def __init__(self, parent, id):
                self.window = wx.Frame.__init__(self, parent, id,'ProgressBar', size=(360, 90), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX)
                status = self.CreateStatusBar()
                panel = wx.Panel(self, pos = (0, 0), size = (100, 300))
                self.progressBar = wx.Gauge(panel, -1, 0, pos=(30, 20), size=(300, 30))
                self.SetStatusText("Please Wait ... Uploading is in progress")
                self.Bind(wx.EVT_CLOSE, self.OnClose)
                
        def update(self, gameSize, gamepath, total, arduinoport, mainFrame):
                self.progressBar.SetRange(gameSize)
                mainFrame.setButtonDisable()
                car = ''
                
                for x in range(0, gameSize):
                        car = gamepath.read(1)
                        arduinoport.write(car)
                        #time.sleep(0.006)
                        
                        self.progressBar.SetValue(x)
                        self.Refresh()

                self.SetStatusText("Uploading is almost finished ... ")
                time.sleep(2)
                self.SetStatusText("Uploading complete.")
                
                mainFrame.setButtonEnable()
                arduinoport.close()
                gamepath.close()
                self.Destroy()
                return

        def OnClose(self, evt):
                return
                
class starter(threading.Thread):
        def __init__(self, threadID, name, counter):
                threading.Thread.__init__(self)
                frame = programmer_gui(parent = None, id = -1)
                frame.Show()
        def run(self):
                pass
                
if __name__ == '__main__':
        app = wx.PySimpleApp()
        # Create new threads
        thread1 = starter(1, "Thread-1", 1)

        # Start new Threads
        thread1.start() 
        app.MainLoop()          
        

