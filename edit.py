'''
Defines a dialog box for the user to edit a flight.
'''
import wx


class EditDialog(wx.Dialog):
    '''
    Allows the user to edit a flight that's been entered.
    '''

    def __init__(self, flight, *args, **kwargs):
        '''
        Creates a new dialog box bound to the given flight. Extra
        arguments are passed along to the wx.Dialog constructor.
        '''
        wx.Dialog.__init__(self, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.quick_field = wx.TextCtrl(parent=self)

        button_sizer = wx.StdDialogButtonSizer()

        button = wx.Button(parent=self, id=wx.ID_OK)
        button.SetDefault()
        button_sizer.AddButton(button)

        button = wx.Button(parent=self, id=wx.ID_CANCEL)
        button_sizer.AddButton(button)
        button_sizer.Realize()

        sizer.Add(self.quick_field)
        sizer.Add(button_sizer)
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.flight = flight
