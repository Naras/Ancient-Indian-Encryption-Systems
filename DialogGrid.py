__author__ = 'naras_mg'
import tkSimpleDialog
# import tkStretchableDialog
from Tkinter import *
import Tix, tkMessageBox

class Init(tkSimpleDialog.Dialog):
    def body(self, master):
        self.Row = Tix.IntVar()
        self.Column = Tix.IntVar()
        self.Row.set(55)
        self.Column.set(75)
        # Label(master, text="Rows:").grid(row=0,sticky=W)
        self.e1 = Entry(master)
        self.row = Tix.Control(master, label='Row', variable=self.Row, \
                              min=1, max=100, integer=1, options='entry.width 10 label.width 20 label.anchor e')
        self.col = Tix.Control(master, label='Column', variable=self.Column, \
                              min=1, max=100, integer=1, options='entry.width 10 label.width 20 label.anchor e')
        self.row.grid(row=0, column=1)
        self.col.grid(row=0, column=2)
        return self.e1 # initial focus
    def validate(self):
        try:
            # self.name = self.e1.get()
            self.result = self.Row.get(), self.Column.get()
            return 1
        except ValueError:
            tkMessageBox.showwarning("Invalid input","Illegal values, try again")
            return 0

class chkbx:
    def __init__(self,parent):
        self.v = IntVar()
        self.chk = Checkbutton(parent,variable=self.v)