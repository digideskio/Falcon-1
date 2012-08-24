import os
import wx
import datetime

import menu
import schedule
import edit
import flight


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

    def AddFlight(self, entry):
        try:
            self.FlightsList.AddFlight(entry)
        except ValueError, e:
            self.ErrorMessageBox('Error adding flight', e.message)

    def FileCommand(self, id):
        try:
            self.FlightsList.FileCommand(id)
        except IOError, err:
            self.ErrorMessageBox('File error', err.message)

    def ErrorMessageBox(self, title, message):
        dialog = wx.MessageDialog(self, message, title,
                                  wx.OK | wx.ICON_ERROR)
        dialog.ShowModal()
        dialog.Destroy()


class FlightsList(wx.HtmlListBox):
    INITIAL_LENGTH = 100

    def __init__(self, *args, **kwargs):
        wx.HtmlListBox.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        # TODO: separate data from user interface
        self.schedule = schedule.Schedule()
        self.Refresh()

    def OnGetItem(self, n):
        return self.Format(self.schedule.get(n))

    def Format(self, entry):
        return entry.report(self.schedule)

    def Refresh(self):
        self.SetItemCount(self.schedule.num_flights(
                first=FlightsList.INITIAL_LENGTH))
        self.RefreshAll()

    def AddFlight(self, entry):
        self.schedule.add(flight.from_line(entry, self.schedule.context()))
        self.Refresh()

    def FileCommand(self, id):
        try:
            {
                wx.ID_NEW: self.OnNew,
                wx.ID_OPEN: self.OnOpen,
                wx.ID_SAVE: self.OnSave,
                wx.ID_SAVEAS: self.OnSaveAs,
            }[id]()
        except KeyError:
            raise KeyError('Unrecognized file command: %s' % str(id))

        self.Refresh()

    def OnNew(self):
        if self.PromptToSave() != wx.ID_CANCEL:
            self.schedule = schedule.Schedule()

    def OnOpen(self):
        if self.PromptToSave() != wx.ID_CANCEL:
            filename = self.PromptForFile(wx.FD_OPEN)
            if filename is not None:
                self.schedule = schedule.Schedule(filename)

    def OnSave(self):
        if self.schedule.filename is None:
            self.OnSaveAs()
        else:
            self.schedule.save()

    def OnSaveAs(self):
        filename = self.PromptForFile(wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if filename is not None:
            self.schedule.save(filename)

    def PromptForFile(self, mode):
        wildcard = 'Itinerary text file (*.txt)|*.txt|' \
                   'All files (*.*)|*.*'
        dialog = wx.FileDialog(self, defaultDir=os.getcwd(),
                               wildcard=wildcard,
                               style=mode | wx.FD_CHANGE_DIR)
        filename = None
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetPath()
        dialog.Destroy()
        return filename

    def PromptToSave(self):
        result = wx.NO
        if self.schedule.modified:
            dialog = wx.MessageDialog(self,
                    '"%s" has been modified.  ' \
                    'Would you like to save it first?' %
                    self.schedule.filename,
                    'File has been changed',
                    wx.YES_NO | wx.CANCEL)
            result = dialog.ShowModal()
            if result == wx.YES:
                self.OnSave()

        return result

    def OnContextMenu(self, e):
        item = self.HitTest(self.ScreenToClient(e.GetPosition()))
        self.Selection = item
        self.Refresh()

        if not hasattr(self, 'itemContext'):
            menuItems = [
                (wx.ID_EDIT,),
                (wx.ID_DELETE,),
            ]

            self.itemContext = menu.create_menu(wx.Menu, menuItems)
            self.Bind(wx.EVT_MENU, self.OnMenuEvent)

        self.PopupMenu(self.itemContext)

    def OnMenuEvent(self, e):
        try:
            {
                wx.ID_DELETE: self.DeleteFlight,
                wx.ID_EDIT: self.EditFlight,
            }[e.Id](self.Selection)
        except KeyError:
            raise AssertionError('Unrecognized file command: %s' % str(id))

    def DeleteFlight(self, index):
        self.schedule.remove(index)
        self.Refresh()

    def EditFlight(self, index):
        edit.EditDialog(self.schedule.get(index), parent=self).Show()


class NewFlight(object):
    def __init__(self, listview):
        self.listview = listview
        context_flight = None
        try:
            context_flight = listview.schedule.get(0)
        except IndexError:
            self.dept_time = datetime.datetime.now()
            self.line = ''
        else:
            self.dept_time = context_flight.dept_time
            self.line = str(context_flight)

    def assign(self, other):
        self.listview.schedule.add(other)
        self.listview.Refresh()

    def __str__(self):
        return self.line


class AddPanel(wx.Panel):  # TODO: change to true panel
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.add_button = wx.Button(parent=self, label='Add Flight')
        self.quick_add = wx.TextCtrl(parent=self, style=wx.TE_PROCESS_ENTER)

        self.Bind(wx.EVT_BUTTON, self.OnAddFlight, self.add_button)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter, self.quick_add)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.add_button, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add((10, 0))
        sizer.Add(wx.StaticText(parent=self, label='Quick add: '),
                  flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.quick_add, flag=wx.ALIGN_CENTER_VERTICAL,
                  proportion=1)
        self.SetSizerAndFit(sizer)

    def OnEnter(self, dummy_event):
        self.GetParent().AddFlight(self.quick_add.GetValue())

    def OnAddFlight(self, dummy_event):
        new_flight = NewFlight(self.GetParent().FlightsList)
        edit.EditDialog(new_flight, parent=self.GetParent()).Show()
