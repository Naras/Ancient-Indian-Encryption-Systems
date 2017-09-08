#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'naras_mg'
from BaseModel import *
from HideRevealRoutines import *

from wx.lib.scrolledpanel import *

import wx, copy, logging

global grid

logging.basicConfig(level=logging.DEBUG,filename='Samjna.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

class DialogCreateGrid(wx.Dialog):
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Create Grid")

        pnl = wx.Panel(self)
        # vbox = wx.BoxSizer(wx.VERTICAL)

        # sb = wx.StaticBox(pnl, label='Grid Size')
        # sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        wx.StaticBox(pnl, label='Set Grid Size', pos=(5, 10), size=(1540, 170))
        lblRows = wx.StaticText(pnl, label='Rows', pos=(15, 35))
        # self.txtRows = wx.StaticText(pnl, label='10', pos=(55, 35))
        sldRows = wx.Slider(pnl, value=10, minValue=1, maxValue=500, pos=(110, 35),
            size=(250, -1), style=wx.SL_HORIZONTAL)
        self.scRows = wx.SpinCtrl(pnl, value='10', pos=(55, 35), size=(60, -1))
        self.scRows.SetRange(1, 1000)
        lblCols = wx.StaticText(pnl, label='Cols', pos=(15, 85))
        # self.txtCols = wx.StaticText(pnl, label='10', pos=(55, 85))
        sldCols = wx.Slider(pnl, value=10, minValue=1, maxValue=500, pos=(110, 85),
            size=(250, -1), style=wx.SL_HORIZONTAL)
        self.scCols = wx.SpinCtrl(pnl, value='10', pos=(55, 85), size=(60, -1))
        self.scCols.SetRange(1, 1000)
        sldRows.Bind(wx.EVT_SCROLL, self.OnSliderScrollRows)
        sldCols.Bind(wx.EVT_SCROLL, self.OnSliderScrollCols)

        # okButton = wx.Button(self, wx.ID_OK)
        okButton = wx.Button(pnl, wx.ID_OK, pos=(30,110))

        # pnl.SetSizer(sbs)

        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # hbox2.Add(okButton, 0, wx.ALL|wx.CENTER, 5)
        # vbox.Add(pnl, proportion=1,
        #     flag=wx.ALL|wx.EXPAND, border=5)
        # vbox.Add(hbox2,
        #     flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        #
        # self.SetSizer(vbox)

    def OnSliderScrollRows(self, e):
        global rows
        obj = e.GetEventObject()
        val = obj.GetValue()
        # self.txtRows.SetLabel(str(val))
        self.scRows.SetValue(val)
        rows = val
    def OnSliderScrollCols(self, e):
        global cols
        obj = e.GetEventObject()
        val = obj.GetValue()
        # self.txtCols.SetLabel(str(val))
        self.scCols.SetValue(val)
        cols = val
class BlockWindow(wx.Panel):
    def __init__(self, parent, ID=-1, label="", pos=wx.DefaultPosition, size=(20, 15)):
        wx.Panel.__init__(self, parent, ID, pos, size, wx.RAISED_BORDER, label)
        self.label = label
        self.SetBackgroundColour("white")
        self.SetMinSize(size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        sz = self.GetClientSize()
        dc = wx.PaintDC(self)
        w,h = dc.GetTextExtent(self.label)
        dc.SetFont(self.GetFont())
        dc.DrawText(self.label, (sz.width-w)/2, (sz.height-h)/2)
class DialogShowGrid(wx.Frame):
    def __init__(self):
        global grid
        wx.Frame.__init__(self, None, -1, "Grid Content")
        self.panel = bwPanel(self,None)
class bwPanel(ScrolledPanel):
    def __init__(self, parent, size=wx.DefaultSize):
        global grid
        ScrolledPanel.__init__(self, parent, size=size)

        self.pal_height = 30

        size_xy = grid.size()
        rows,cols = size_xy.getx(),size_xy.gety()

        self.sizer = wx.FlexGridSizer(rows=rows, cols=cols, hgap=1, vgap=1)
        for r in range(rows):
            for c in range(cols):
                cell=grid.get_at(xy(r,c))
                if cell.isEmpty(): cellContent='.'
                else: cellContent = cell
                bw = BlockWindow(self, label=str(cellContent))
                self.sizer.Add(bw, 0,  0)

        self.sizer.AddGrowableCol(0,1)
        self.sizer.AddGrowableCol(1,2)
        self.sizer.SetFlexibleDirection(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.SetupScrolling()
class DialogHideRevealText(wx.Dialog):
    def __init__(self):
        global grid
        wx.Dialog.__init__(self, None, title="Plain Text")
        f = open('Plain.txt')
        plain = f.readlines()
        f.close()
        self.pnl = wx.Panel(self)
        okBtn =  wx.Button(self.pnl, wx.ID_OK, pos=(60, 190))
        hideBtn =  wx.Button(self.pnl, wx.ID_ANY, pos=(150, 190), label='Hide text')
        hideBtn.Bind(wx.EVT_BUTTON,self.OnHide)
        revealBtn =  wx.Button(self.pnl, wx.ID_ANY, pos=(240, 190), label='Reveal text')
        revealBtn.Bind(wx.EVT_BUTTON,self.OnReveal)
        lblLength = wx.StaticText(self.pnl, label='Plain Text Length', pos=(340, 190))
        self.scTextLength = wx.SpinCtrl(self.pnl, value='0', pos=(430, 190), size=(40, -1))

        lblText = wx.StaticText(self.pnl, label='Select Text', pos=(90, 15))
        self.cb = wx.ComboBox(self.pnl, pos=(80, 30), choices=plain,
            style=wx.CB_READONLY)
        self.cb.SetSelection(0)

        lblBandha = wx.StaticText(self.pnl, label='Select Bandha', pos=(320, 15))
        self.bandhas = ['row by row', 'mukha bandha', 'diagonal']
        self.cbBandha = wx.ComboBox(self.pnl, pos=(300, 30), choices=self.bandhas,
            style=wx.CB_READONLY)
        self.cbBandha.SetSelection(0)

        lblStart = wx.StaticText(self.pnl, label='Start Cell', pos=(35, 60))
        self.scStartX = wx.SpinCtrl(self.pnl, value='0', pos=(85, 60), size=(40, -1))
        self.scStartX.SetRange(0, 1000)
        sldRows = wx.Slider(self.pnl, value=10, minValue=0, maxValue=1000, pos=(120, 60),
            size=(250, -1), style=wx.SL_HORIZONTAL)

        self.scStartY = wx.SpinCtrl(self.pnl, value='0', pos=(85, 80), size=(40, -1))
        self.scStartY.SetRange(0, 1000)
        sldCols = wx.Slider(self.pnl, value=10, minValue=0, maxValue=1000, pos=(120, 80),
            size=(250, -1), style=wx.SL_HORIZONTAL)

        lblSelectedText = wx.StaticText(self.pnl, label='Selected Text   -> ', pos=(5, 140))
        self.st = wx.StaticText(self.pnl, label=plain[0], pos=(110, 140))
        lblSelected = wx.StaticText(self.pnl, label='Selected Bandha ->', pos=(5, 160))
        self.stBandha = wx.StaticText(self.pnl, label=self.bandhas[0], pos=(110, 160))

        self.cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.cbBandha.Bind(wx.EVT_COMBOBOX, self.OnSelectBandha)
        sldRows.Bind(wx.EVT_SCROLL, self.OnSliderScrollRows)
        sldCols.Bind(wx.EVT_SCROLL, self.OnSliderScrollCols)

        self.lblStatus_text = wx.StaticText(self.pnl, label='Status ', pos=(15, 220), style = wx.ALIGN_LEFT)
        self.lblStatus_pos = wx.StaticText(self.pnl, label='Status ', pos=(15, 240), style = wx.ALIGN_LEFT)

        self.SetSize((550, 300))
        self.SetTitle('Available Plain Text')
        self.Centre()
        self.Show(True)

    def OnHide(self,e):
        status_text = self.st.GetLabel()
        x = self.scStartX.GetValue()
        y = self.scStartY.GetValue()
        bandhaText = self.cbBandha.GetValue()
        # print bandhaText
        if bandhaText == self.bandhas[0]: hide_inplace(grid,grid.rowByrowBandha(xy(x,y)),status_text[:-1])
        elif bandhaText == self.bandhas[1]: hide_inplace(grid,grid.mukhaBandha(xy(x,y)),status_text[:-1])
        else: hide_inplace(grid,grid.diagonalBandha(xy(x,y)),status_text[:-1])
        self.lblStatus_text.SetLabel( 'Hid text:  '+ status_text)
        self.lblStatus_text.SetForegroundColour('blue')
        self.lblStatus_pos.SetLabel( 'at position:' + str(xy(x,y)) + ' .. with Bandha:  ' + bandhaText)
        self.scTextLength.SetValue(len(status_text))
    def OnReveal(self,e):
        status_text = self.st.GetLabel()
        x = self.scStartX.GetValue()
        y = self.scStartY.GetValue()
        bandhaText = self.cbBandha.GetValue()
        length = self.scTextLength.GetValue()
        # print bandhaText
        if bandhaText == self.bandhas[0]: status_text = reveal(grid,grid.rowByrowBandha(xy(x,y)), length)
        elif bandhaText == self.bandhas[1]: status_text = reveal(grid,grid.mukhaBandha(xy(x,y)), length)
        else: status_text = reveal(grid,grid.diagonalBandha(xy(x,y)), length)
        self.lblStatus_text.SetLabel( 'Plain text is:  '+ status_text)
        self.lblStatus_text.SetForegroundColour('red')
        self.lblStatus_pos.SetLabel( 'at position:' + str(xy(x,y)) + ' .. with Bandha:  ' + bandhaText)
        self.st.SetLabel('')
        self.cb.SetSelection(-1)
    def OnSelect(self, e):
        i = e.GetString()
        self.st.SetLabel(i)
        self.scTextLength.SetValue(len(i))
    def OnSelectBandha(self, e):
        i = e.GetString()
        self.stBandha.SetLabel(i)
    def OnSliderScrollRows(self, e):
        global rows
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.scStartX.SetValue(val)
        rows = val
    def OnSliderScrollCols(self, e):
        global cols
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.scStartY.SetValue(val)
        cols = val

class Main(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Main, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        gridMenu = wx.Menu()
        eximMenu = wx.Menu()
        viewMenu = wx.Menu()

        self.createGrid = gridMenu.Append(wx.ID_ANY,'&create')

        self.prepPlain = gridMenu.Append(wx.ID_ANY,'&hide/reveal ')
        self.prepPlain.Enable(False)

        self.showGrid = gridMenu.Append(wx.ID_ANY,'&show grid')
        self.showGrid.Enable(False)
        self.showGridObscured = gridMenu.Append(wx.ID_ANY,'show grid with &noise')
        self.showGridObscured.Enable(False)
        # self.exitGrid = gridMenu.Append(wx.ID_ANY,'e&xit')
        self.eximExport = eximMenu.Append(wx.ID_ANY,'export')
        self.eximExport.Enable(False)
        self.eximImport = eximMenu.Append(wx.ID_ANY,'import')
        # self.eximImport.Enable(False)

        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar',
            'Show Statusbar', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)

        menubar.Append(gridMenu, '&Grid')
        menubar.Append(eximMenu, '&Export/Import')
        menubar.Append(viewMenu, '&View')

        self.Bind(wx.EVT_MENU, self.GridCreate, self.createGrid)
        self.Bind(wx.EVT_MENU, self.GridShow, self.showGrid)
        self.Bind(wx.EVT_MENU, self.GridObscure, self.showGridObscured)
        self.Bind(wx.EVT_MENU, self.hide_revealText, self.prepPlain)

        self.Bind(wx.EVT_MENU, self.GridExport,self.eximExport)
        self.Bind(wx.EVT_MENU, self.GridImport,self.eximImport)
        self.SetMenuBar(menubar)

        # self.toolbar = self.CreateToolBar()
        # self.toolbar.AddLabelTool(1, '', wx.Bitmap('exit.png'))
        # self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((350, 250))
        self.SetTitle('Check menu item')
        self.Centre()
        self.Show(True)

    def GridCreate(self, e):
        global grid
        dlg = DialogCreateGrid()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            # colsize,rowsize = dlg.txtRows.GetLabel(), dlg.txtCols.GetLabel()
            colsize,rowsize = dlg.scRows.GetValue(), dlg.scCols.GetValue()
        dlg.Destroy()
        grid = CellGrid(int(colsize),int(rowsize))

        self.statusbar.SetStatusText("created grid rowsize %s, colsize %s" % (rowsize, colsize))
        self.prepPlain.Enable(True)
        self.showGrid.Enable(True)
        self.showGridObscured.Enable(True)
        self.eximExport.Enable(True)
        self.eximImport.Enable(True)
    def GridShow(self, e):
        global grid
        dlg = DialogShowGrid()
        res = dlg.Show()
        self.statusbar.SetStatusText('phew! that took a long time!')
    def GridObscure(self, e):
        global grid
        gridLocal = copy.deepcopy(grid)
        grid.get().fillRandomNulls()
        dlg = DialogShowGrid()
        res = dlg.Show()
        grid = copy.deepcopy(gridLocal)
        del gridLocal
        self.statusbar.SetStatusText('obscured!')
    def hide_revealText(self, e):
        global grid
        bandhas = ['row by row', 'mukha bandha', 'diagonal']
        dlg = DialogHideRevealText()
        res = dlg.ShowModal()
        if res == wx.ID_OK: pass
            # status_text = dlg.st.GetLabel()
            # x = dlg.scStartX.GetValue()
            # y = dlg.scStartY.GetValue()
            # bandhaText = dlg.cbBandha.GetValue()
            # # print bandhaText
            # if bandhaText == bandhas[0]: hide(grid,grid.rowByrowBandha(xy(x,y)),status_text[:-1])
            # elif bandhaText == bandhas[1]: hide(grid,grid.mukhaBandha(xy(x,y)),status_text[:-1])
            # else: hide(grid,grid.diagonalBandha(xy(x,y)),status_text[:-1])
        # else: status_text = 'No plain text selected!'
        dlg.Destroy()
        # self.statusbar.SetStatusText(status_text)
    def GridExport(self, e):
        global grid
        exportTofile(grid,'export.txt')
    def GridImport(self, e):
        global grid
        grid = importFromfile('export.txt')
        self.prepPlain.Enable(True)
        self.showGrid.Enable(True)
        self.showGridObscured.Enable(True)
        self.eximExport.Enable(True)

    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

def main():

    ex = wx.App()
    Main(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
