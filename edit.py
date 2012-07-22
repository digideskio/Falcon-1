'''
Defines a dialog box for the user to edit a flight.
'''
import wx
import flight


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

        self.SetTitle('Edit flight')

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.quick_field = wx.TextCtrl(parent=self)
        self.quick_field.SetValue(str(flight))
        '''
        controls_sizer = wx.GridSizer(2, 6)
        arrive_label = wx.StaticText(self, 'Departs')
        arrive_combo = wx.ComboBox(self, value=self.flight.wx.CB)
        '''
        button_sizer = wx.StdDialogButtonSizer()

        button = wx.Button(parent=self, id=wx.ID_OK)
        button.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OkButton, button)
        button_sizer.AddButton(button)

        button = wx.Button(parent=self, id=wx.ID_CANCEL)
        button_sizer.AddButton(button)
        self.Bind(wx.EVT_BUTTON, self.CancelButton, button)
        button_sizer.Realize()

        sizer.Add(self.quick_field, flag=wx.GROW | wx.ALL, border=5)
        sizer.Add(button_sizer)
        # sizer.Add(controls_sizer)

        self.SetSizer(sizer)
        sizer.Fit(self)

        self.flight = flight

    def OkButton(self, _evt):
        try:
            self.flight.assign(flight.from_line(self.quick_field.GetValue()))
        except ValueError, err:
            self.ErrorMessageBox("Invalid flight string", err.message)
        else:
            self.GetParent().Refresh()
            self.Destroy()

    def CancelButton(self, _evt):
        self.Destroy()

    def ErrorMessageBox(self, title, message):
        # TODO: refactor (duplicated in listview)
        dialog = wx.MessageDialog(self, message, title,
                                  wx.OK | wx.ICON_ERROR)
        dialog.ShowModal()
        dialog.Destroy()
