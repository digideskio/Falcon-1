import wx


def create_menu(cls, items):
    newMenu = cls()
    build_menu(newMenu, items)
    return newMenu


def build_menu(curr, items):
    for item in items:
        if len(item) == 2 and isinstance(item[1], list):
            submenu = wx.Menu()
            build_menu(submenu, item[1])
            curr.Append(submenu, item[0])
        elif item:
            curr.Append(*item)
        else:
            curr.AppendSeparator()


ID_IMPORT = wx.ID_HIGHEST + 1
