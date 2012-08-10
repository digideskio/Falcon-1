'''
Defines a dialog box for the user to edit a flight.
'''
import wx
import flight
from wx.lib import masked
from flight import format_date, format_time
from flight import string_to_datetime, datetime_to_wx
from airport import NoSuchAirportError
import airport


# TODO: move out into utility module
def set_property(name):
    def decorator(method):
        def fget(self):
            return getattr(self, name)

        def fset(self, other):
            setattr(self, name, other)
            method(self)

        return property(fget=fget, fset=fset)

    return decorator


def string_to_wx_datetime(date_string, context):
    return datetime_to_wx(string_to_datetime(date_string, context))


def set_date(wx_datetime, date):
    wx_datetime.SetDay(date.GetDay())
    wx_datetime.SetMonth(date.GetMonth())
    wx_datetime.SetYear(date.GetYear())


def set_time(wx_datetime, time):
    wx_datetime.SetHour(time.GetHour())
    wx_datetime.SetMinute(time.GetMinute())
    wx_datetime.SetSecond(time.GetSecond())


class ProxyFlight(object):
    LINE_CHANGED = object()
    COMPONENT_CHANGED = object()

    def __init__(self, line, context):
        self.context = context
        self._line = line

        # help out the code analysis tools
        (self._departs, self._arrives,
         self._dept_time, self._arr_time) = None, None, None, None
        self.listeners = []

        self._split_line()

    def _split_line(self):
        components = flight.parse_line(self._line)

        (self._departs, self._arrives) = (components['departs'],
                                          components['arrives'])
        self._dept_time = string_to_wx_datetime(components['dept_time'],
                                                self.context)
        self._arr_time = string_to_wx_datetime(components['arr_time'],
                                               self.context)

    def _compute_line(self):
        values = {
            'departs': self.departs,
            'dept_time': ' '.join((format_date(self.dept_time),
                                       format_time(self.dept_time))),
            'arrives': self.arrives,
            'arr_time': ' '.join((format_date(self.arr_time),
                                      format_time(self.arr_time))),
        }
        self._line = ('%(departs)s %(dept_time)s %(arrives)s %(arr_time)s' %
                      values)

    @set_property('_line')
    def line(self):
        self.update(ProxyFlight.COMPONENT_CHANGED)

    @set_property('_departs')
    def departs(self):
        self.update(ProxyFlight.LINE_CHANGED)

    @set_property('_arrives')
    def arrives(self):
        self.update(ProxyFlight.LINE_CHANGED)

    @set_property('_dept_time')
    def dept_time(self):
        self.update(ProxyFlight.LINE_CHANGED)

    def set_dept_date(self, date):
        set_date(self._dept_time, date)
        self.update(ProxyFlight.LINE_CHANGED)

    def set_dept_time(self, time):
        set_time(self._dept_time, time)
        self.update(ProxyFlight.LINE_CHANGED)

    @set_property('_arr_time')
    def arr_time(self):
        self.update(ProxyFlight.LINE_CHANGED)

    def set_arr_date(self, date):
        set_date(self._arr_time, date)
        self.update(ProxyFlight.LINE_CHANGED)

    def set_arr_time(self, time):
        set_time(self._arr_time, time)
        self.update(ProxyFlight.LINE_CHANGED)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def update(self, event):
        if event is ProxyFlight.COMPONENT_CHANGED:
            self._split_line()
        elif event is ProxyFlight.LINE_CHANGED:
            self._compute_line()

        for listener in self.listeners:
            listener.on_update(event)

    def to_flight(self):
        return flight.from_line(self._line)

    @classmethod
    def from_flight(cls, other):
        return ProxyFlight(str(other), other.dept_time)


class EditDialog(wx.Dialog):
    '''
    Allows the user to edit a flight that's been entered.
    '''

    def __init__(self, tracked_flight, *args, **kwargs):
        '''
        Creates a new dialog box bound to the given flight. Extra
        arguments are passed along to the wx.Dialog constructor.
        '''
        wx.Dialog.__init__(self, *args, **kwargs)

        self.flight = tracked_flight
        self.proxy_flight = ProxyFlight.from_flight(tracked_flight)
        self.proxy_flight.add_listener(self)

        self.updating_controls = False
        self.updating_line = False

        self.SetTitle('Edit flight')

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.quick_field = wx.TextCtrl(parent=self)
        self.quick_field.SetValue(self.proxy_flight.line)
        self.Bind(wx.EVT_TEXT, self.QuickFieldChanged, self.quick_field)

        controls_sizer = wx.FlexGridSizer(2, 6, 5, 5)
        controls_sizer.Add(wx.StaticText(self, label='Departs'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.departs_combo = wx.ComboBox(self, value=self.flight.departs.code)
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
        self.arrives_combo = wx.ComboBox(self, value=self.flight.arrives.code)
        controls_sizer.Add(self.arrives_combo)
        controls_sizer.Add(wx.StaticText(self, label='on'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.arr_date_picker = wx.DatePickerCtrl(self, style=wx.DP_DROPDOWN)
        controls_sizer.Add(self.arr_date_picker)
        controls_sizer.Add(wx.StaticText(self, label='at'),
                           flag=wx.ALIGN_CENTER_VERTICAL)
        self.arr_time_picker = masked.TimeCtrl(self, format='24HHMM')
        controls_sizer.Add(self.arr_time_picker)

        self.UpdateControls()

        self.Bind(wx.EVT_TEXT, self.DepartsComboChanged, self.departs_combo)
        self.Bind(wx.EVT_DATE_CHANGED, self.DeptDatePickerChanged,
                  self.dept_date_picker)
        self.Bind(masked.EVT_TIMEUPDATE, self.DeptTimePickerChanged,
                  self.dept_time_picker)
        self.Bind(wx.EVT_TEXT, self.ArrivesComboChanged, self.arrives_combo)
        self.Bind(wx.EVT_DATE_CHANGED, self.ArrDatePickerChanged,
                  self.arr_date_picker)
        self.Bind(masked.EVT_TIMEUPDATE, self.ArrTimePickerChanged,
                  self.arr_time_picker)

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

    def OkButton(self, _evt):
        try:
            self.flight.assign(self.proxy_flight.to_flight())
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

    def DepartsComboChanged(self, _evt):
        self.proxy_flight.departs = self.departs_combo.GetValue()

    def DeptDatePickerChanged(self, _evt):
        self.proxy_flight.set_dept_date(self.dept_date_picker.GetValue())

    def DeptTimePickerChanged(self, _evt):
        self.proxy_flight.set_dept_time(self.dept_time_picker.GetWxDateTime())

    def ArrivesComboChanged(self, _evt):
        self.proxy_flight.arrives = self.arrives_combo.GetValue()

    def ArrDatePickerChanged(self, _evt):
        self.proxy_flight.set_arr_date(self.arr_date_picker.GetValue())

    def ArrTimePickerChanged(self, _evt):
        self.proxy_flight.set_arr_time(self.arr_time_picker.GetWxDateTime())

    def QuickFieldChanged(self, evt):
        try:
            self.proxy_flight.line = evt.GetString()
            self.quick_field.SetBackgroundColour(wx.Colour(127, 255, 127))
        except ValueError:
            self.quick_field.SetBackgroundColour(wx.Colour(255, 127, 127))

        self.quick_field.Refresh()

    def on_update(self, event):
        if event == ProxyFlight.LINE_CHANGED:
            if not self.updating_controls:
                self.updating_line = True
                self.quick_field.SetValue(self.proxy_flight.line)
                self.updating_line = False
        elif event == ProxyFlight.COMPONENT_CHANGED:
            if not self.updating_line:
                self.updating_controls = True
                self.UpdateControls()
                self.updating_controls = False

    def UpdateControls(self):
        self.departs_combo.SetValue(self.proxy_flight.departs)
        try:
            airport.get_airport(self.proxy_flight.departs)
        except NoSuchAirportError:
            self.departs_combo.SetBackgroundColour(wx.Colour(255, 255, 127))
        else:
            self.departs_combo.SetBackgroundColour(wx.WHITE)

        self.dept_date_picker.SetValue(self.proxy_flight.dept_time)
        self.dept_time_picker.SetWxDateTime(self.proxy_flight.dept_time)
        self.arrives_combo.SetValue(self.proxy_flight.arrives)
        try:
            airport.get_airport(self.proxy_flight.arrives)
        except NoSuchAirportError:
            self.arrives_combo.SetBackgroundColour(wx.Colour(255, 255, 127))
        else:
            self.arrives_combo.SetBackgroundColour(wx.WHITE)

        self.arr_date_picker.SetValue(self.proxy_flight.arr_time)
        self.arr_time_picker.SetWxDateTime(self.proxy_flight.arr_time)
