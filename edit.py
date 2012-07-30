'''
Defines a dialog box for the user to edit a flight.
'''
import wx
import flight
from wx.lib import masked


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

        controls_sizer = wx.FlexGridSizer(2, 6, 5, 5)
        controls_sizer.Add(wx.StaticText(self, label='Departs'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.departs_combo = wx.ComboBox(self, value=flight.departs.code)
        controls_sizer.Add(self.departs_combo)
        controls_sizer.Add(wx.StaticText(self, label='on'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.dept_date_picker = wx.DatePickerCtrl(self, style=wx.DP_DROPDOWN)
        controls_sizer.Add(self.dept_date_picker)
        controls_sizer.Add(wx.StaticText(self, label='at'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.dept_time_picker = masked.TimeCtrl(self, format='24HHMM')
        controls_sizer.Add(self.dept_time_picker)

        controls_sizer.Add(wx.StaticText(self, label='Arrives'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.arrives_combo = wx.ComboBox(self, value=flight.arrives.code)
        controls_sizer.Add(self.arrives_combo)
        controls_sizer.Add(wx.StaticText(self, label='on'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.arr_date_picker = wx.DatePickerCtrl(self, style=wx.DP_DROPDOWN)
        controls_sizer.Add(self.arr_date_picker)
        controls_sizer.Add(wx.StaticText(self, label='at'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.arr_time_picker = masked.TimeCtrl(self, format='24HHMM')
        controls_sizer.Add(self.arr_time_picker)

        events = {
            self.departs_combo: wx.EVT_TEXT,
            self.dept_date_picker: wx.EVT_DATE_CHANGED,
            self.dept_time_picker: masked.EVT_TIMEUPDATE,
            self.arrives_combo: wx.EVT_TEXT,
            self.arr_date_picker: wx.EVT_DATE_CHANGED,
            self.arr_time_picker: masked.EVT_TIMEUPDATE,
        }
        for elem in events:
            self.Bind(events[elem], self.ControlChanged, elem)

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
        sizer.Add(controls_sizer, flag=wx.ALL, border=5)
        sizer.Add(button_sizer, flag=wx.ALL | wx.ALIGN_RIGHT, border=5)

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

    def ControlChanged(self, e):
        # TODO
        pass
