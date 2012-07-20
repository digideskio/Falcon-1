import os
import wx

import menu
import schedule
import edit


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
        self.schedule.add(entry)
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


class AddPanel(wx.TextCtrl):  # TODO: change to true panel
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, style=wx.TE_PROCESS_ENTER, *args, **kwargs)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

    def OnEnter(self, dummy_event):
        self.GetParent().AddFlight(self.GetValue())
