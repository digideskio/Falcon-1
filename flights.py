import wx
import files

class FlightsPanel(wx.Panel):
	def __init__(self, *args, **kwargs):
		wx.Panel.__init__(self, *args, **kwargs)
		
		self.MainSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.AddPanel = AddPanel(parent=self)
		self.MainSizer.Add(self.AddPanel, border=4, proportion=0,
				flag=wx.EXPAND | wx.ALL)
		
		self.FlightsList = FlightsList(parent=self)
		self.MainSizer.Add(self.FlightsList, border=4, proportion=1,
				flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)
		
		self.SetAutoLayout(True)
		self.SetSizer(self.MainSizer)
		self.Layout()
		
		self.Bind(wx.EVT_SIZE, self.OnSize)
	
	def OnSize(self, e):
		self.SetSize(e.GetSize())
		self.Layout()

class FlightsList(wx.HtmlListBox):
    INITIAL_LENGTH = 100

    def __init__(self, *args, **kwargs):
        wx.HtmlListBox.__init__(self, *args, **kwargs)
        self.Refresh()
        
    def OnGetItem(self, n):
        return self.Format(files.get_flight(n))
        
    def Format(self, flight):
        return '<font color="green">' + str(flight) + '</font>' # TODO: expand

    def Refresh(self):
        self.SetItemCount(len(files.get_flights(first=FlightsList.INITIAL_LENGTH)))
        self.RefreshAll()

class AddPanel(wx.TextCtrl): # TODO: change to true panel
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, style=wx.TE_PROCESS_ENTER, *args, **kwargs)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
    
    def OnEnter(self, e):
        files.add_flight(self.GetValue())
        self.GetParent().FlightsList.Refresh()
