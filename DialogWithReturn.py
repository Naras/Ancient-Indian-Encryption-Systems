__author__ = 'naras_mg'
import wx

########################################################################
global rows
global cols
rows = 10
cols = 10
class MyDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Dialog")

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Grid Size')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        wx.StaticBox(pnl, label='Set Grid Size', pos=(5, 10), size=(1540, 170))
        lblRows = wx.StaticText(pnl, label='Rows', pos=(15, 35))
        self.txtRows = wx.StaticText(pnl, label='10', pos=(55, 35))
        sldRows = wx.Slider(pnl, value=10, minValue=1, maxValue=500, pos=(85, 35),
            size=(250, -1), style=wx.SL_HORIZONTAL)
        lblCols = wx.StaticText(pnl, label='Cols', pos=(15, 85))
        self.txtCols = wx.StaticText(pnl, label='10', pos=(55, 85))
        sldCols = wx.Slider(pnl, value=10, minValue=1, maxValue=500, pos=(85, 85),
            size=(250, -1), style=wx.SL_HORIZONTAL)
        sldRows.Bind(wx.EVT_SCROLL, self.OnSliderScrollRows)
        sldCols.Bind(wx.EVT_SCROLL, self.OnSliderScrollCols)
        pnl.SetSizer(sbs)

        okButton = wx.Button(self, wx.ID_OK)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(okButton, 0, wx.ALL|wx.CENTER, 5)
        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
    def OnSliderScrollRows(self, e):
        global rows
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.txtRows.SetLabel(str(val))
        rows = val
    def OnSliderScrollCols(self, e):
        global cols
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.txtCols.SetLabel(str(val))
        cols = val
    def OnOk(self,e):
        global rows
        global cols
        return rows ,cols
    # def OnClose(self, e):
    #     self.Destroy()

########################################################################
class MainProgram(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Main Program")
        panel = wx.Panel(self)

        btn = wx.Button(panel, label="Open dialog")
        btn.Bind(wx.EVT_BUTTON, self.onDialog)

        self.Show()

    #----------------------------------------------------------------------
    def onDialog(self, event):
        """"""
        dlg = MyDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            print dlg.txtRows.GetLabel(), dlg.txtCols.GetLabel()
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainProgram()
    app.MainLoop()