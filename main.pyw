#!/usr/bin/python

import wx

import flights

class MainMenu(wx.MenuBar):
	def __init__(self, *args, **kwargs):
		wx.MenuBar.__init__(self, *args, **kwargs)
		
		self.File = wx.Menu()
		self.File.Append(wx.ID_EXIT, 'E&xit\tAlt+F4',
				'Terminate Falcon')
		
		self.Append(self.File, '&File')
	
class MainWindow(wx.Frame):
	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		
		self.Menu = MainMenu()
		self.SetMenuBar(self.Menu)
		
		self.Panel = flights.FlightsPanel(parent=self, id=wx.ID_ANY)
		
		self.SmallIcon = wx.Icon('falcon.ico', wx.BITMAP_TYPE_ICO,
				16, 16) # TODO
		self.LargeIcon = wx.Icon('falcon.ico', wx.BITMAP_TYPE_ICO,
				32, 32)
		self.SetIcon(self.SmallIcon)
		self.SetIcon(self.LargeIcon)
		
		self.SetMinSize(kwargs['size'])
		self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
		
		self.Show()
	
	def OnExit(self, e):
		self.Close(True)

App = wx.App(redirect=False)
MainWnd = MainWindow(parent=None, title='Falcon Flight Tracker', size=(640, 640))
App.MainLoop()
