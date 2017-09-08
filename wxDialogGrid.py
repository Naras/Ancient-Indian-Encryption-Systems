#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
author: Naras M.G
'''

import wx

global rows
global cols
rows = 10
cols = 10
class DialogCreateGrid(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(DialogCreateGrid, self).__init__(*args, **kw)
            
        self.InitUI()
        self.SetSize((350, 200))
        self.SetTitle("Create Grid")
        
        
    def InitUI(self):

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
       
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')

        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

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
        print rows ,cols
    def OnClose(self, e):
        self.Destroy()
    def finalResult(self):
         return rows,cols
        
class Example(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
            
        self.InitUI()
        
        
    def InitUI(self):    
    
        ID_DEPTH = wx.NewId()

        tb = self.CreateToolBar()
        tb.AddLabelTool(id=ID_DEPTH, label='', 
            bitmap=wx.Bitmap('color.png'))
        
        tb.Realize()

        self.Bind(wx.EVT_TOOL, self.OnCreateGrid, 
            id=ID_DEPTH)

        self.SetSize((300, 200))
        self.SetTitle('Create Grid')
        self.Centre()
        self.Show(True)
        
        
    def OnCreateGrid(self, e):
        
        createGrid = DialogCreateGrid(None,
            title='Create Grid')
        createGrid.ShowModal()
        createGrid.Destroy()        


def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()