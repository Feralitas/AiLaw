#!/usr/bin/env python

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.logger import Logger
import datetime
import win32gui
import win32con
import win32api
import kivy.utils
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
import random
#import webview
from kivy.config import Config
import win32com.client
from brAIn import brAIn

Config.set('graphics', 'borderless', 'true')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '300')
Config.set('graphics', 'left', '300')



import sys
import fileinput
import queue
from mouseInterfaces import start_mouse_event_listener_thread, stop_mouse_event_listener_thread, command_queue
from markedtext import get_selected_text


def funktionDieNenStringNimmtUndSieGibtZurueckAnzahlZeilenInAbhaengigkeitDerZeilenbreite(input, mz):
    #Funktionsweiße: Abbau des Strings bis er leer ist. Jedes mal eins dazu Zählen
    az = 0
    counter = 0
    for x in input:
        if (x == '\n'):
            az = az + 1
        counter = counter + 1
        if (counter > mz):
            az = az + 1
            counter = 0
    dieFinaleAnzahlAnZeilenDieManBenoetigtUmDasGanzeDannAuchWirklichSchoenDarZuStellen = az
    
    return dieFinaleAnzahlAnZeilenDieManBenoetigtUmDasGanzeDannAuchWirklichSchoenDarZuStellen

class AFA(App):
    globalText = "test text"
    outTxt = Label(text='Testsss', markup=True, size_hint=(1.0, 1.0), halign="left", valign="middle")
    outTxt.bind(size=outTxt.setter('text_size'))  
    def callbackWriteText(self):
        try:
            cmd = command_queue.get_nowait()
            if cmd == "Gesture button":
                
                self.globalText = get_selected_text() #MW test
                #webview.create_window('AiLaw', self.globalText)
                #webview.start()
                if len(self.globalText) > 0:
                    self.outTxt.text = '[size=16][color=FFFFFF][font=RobotoMono-Regular]'+ brAIn(self.globalText) +'[/font][/color][/size]'
                self.startUp()
                
                self.StatusOfApp = 1
            if cmd == "Program end":
                self.stop()
        except queue.Empty:
            pass

    def getHandleOfThisWindow(self):
        if self.handle == 0:
            self.handle = win32gui.FindWindow(None, "Advocatum facile adiutor")
        return self.handle

    def makeItTransparent(self, alpha):# Set alpha between 0 and 1. 0 no opacity, 1 invisible
        alpha = int((1-alpha) * 255)
        win32gui.SetWindowLong(self.getHandleOfThisWindow(), win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.getHandleOfThisWindow(), win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)   # Make it a layered window
        win32gui.SetLayeredWindowAttributes(self.getHandleOfThisWindow(), win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)        # make it transparent (alpha between 0 and 255)
    
    def makeItForeground(self):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.getHandleOfThisWindow())

    def PositionToMouse(self, width, height):
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        flags, hcursor, (x,y) = win32gui.GetCursorInfo()
        print("height is " + str(funktionDieNenStringNimmtUndSieGibtZurueckAnzahlZeilenInAbhaengigkeitDerZeilenbreite(self.outTxt.text,100)) + 'lines')
        win32gui.SetWindowPos(self.getHandleOfThisWindow(), win32con.HWND_TOP, round(x - width/2), y - height - 80, width, height, win32con.SWP_SHOWWINDOW)
        self.makeItForeground()

    def hibernate(self):
        win32gui.ShowWindow(self.getHandleOfThisWindow(), 0)
        self.StatusOfApp = 0

    def startUp(self):
        win32gui.ShowWindow(self.getHandleOfThisWindow(),1)
        self.PositionToMouse(1030, funktionDieNenStringNimmtUndSieGibtZurueckAnzahlZeilenInAbhaengigkeitDerZeilenbreite(self.outTxt.text,100)*30)
        self.makeItTransparent(.2)
        self.makeItForeground()
        self.makeItForeground()

    def on_stop(self):
        stop_mouse_event_listener_thread()

    def build(self):
        ##Experiment
        self.handle = 0  #init
        self.StatusOfApp = 0
        self.preller = 0
        layout = GridLayout(cols = 1)

        ##Exp End
        self.title = 'Advocatum facile adiutor'
        

        
        layout.add_widget(self.outTxt)


        Clock.schedule_interval(lambda dt: self.callbackWriteText(), 0.01)
        Clock.schedule_once(lambda dt: self.hibernate(), 0.2) # initialiying the hibernate after start up
        return layout


start_mouse_event_listener_thread()

try:
    AFA().run()
except KeyboardInterrupt:
    Logger.info("main: Ctrl+C detected. Terminate!")
    stop_mouse_event_listener_thread()

exit()