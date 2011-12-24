#!/usr/bin/python

import wx

import menu
import listview

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        
        menuItems = [
            ("&File", [
                (wx.ID_NEW, '&New\tCtrl+N',
                    'Start from a blank schedule'),
                (wx.ID_OPEN, '&Open...\tCtrl+O',
                    'Open an existing schedule'),
                (),
                (wx.ID_SAVE, '&Save\tCtrl+S',
                    'Save the current schedule'),
                (wx.ID_SAVEAS, 'Save &As...\tCtrl+Shift+S',
                    'Save the current schedule under a new name'),
                (),
                (wx.ID_EXIT, 'E&xit\tAlt+F4',
                    'Terminate Falcon'),
            ])
        ]
        
        self.Menu = menu.create_menu(wx.MenuBar, menuItems)
        self.SetMenuBar(self.Menu)
        
        self.Panel = listview.FlightsPanel(parent=self, id=wx.ID_ANY)
        
        self.SmallIcon = wx.Icon('falcon.ico', wx.BITMAP_TYPE_ICO,
                16, 16) # TODO
        self.LargeIcon = wx.Icon('falcon.ico', wx.BITMAP_TYPE_ICO,
                32, 32)
        self.SetIcon(self.SmallIcon)
        self.SetIcon(self.LargeIcon)
        
        self.SetMinSize(kwargs['size'])

        self.Bind(wx.EVT_MENU, self.OnMenuEvent)
        
        self.Show()
    
    def OnMenuEvent(self, e):
        if e.Id == wx.ID_EXIT:
            self.Close(True)
        else:
            self.Panel.FileCommand(e.Id)

App = wx.App(redirect=False)
MainWnd = MainWindow(parent=None, title='Falcon Flight Tracker', size=(640, 640))
App.MainLoop()
