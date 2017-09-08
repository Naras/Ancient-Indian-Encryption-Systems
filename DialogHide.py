__author__ = 'naras_mg'
import tkSimpleDialog
# import tkStretchableDialog
from Tkinter import *
import Tix, tkMessageBox

class Init(tkSimpleDialog.Dialog):
    def body(self, master):
        self.Row = Tix.IntVar()
        self.Column = Tix.IntVar()
        self.Length = Tix.IntVar()
        self.Bandha = Tix.StringVar()
        self.Plain = Tix.StringVar()

        self.Row.set(0)
        self.Column.set(0)
        self.Length.set(10)
        self.Bandha.set('Row by Row Bandha')
        self.Plain.set('this is the first message')
        # Label(master, text="Rows:").grid(row=0,sticky=W)
        self.e1 = Entry(master)
        self.row = Tix.Control(master, label='Row', variable=self.Row, \
                              min=0, max=100, integer=1, options='entry.width 10 label.width 20 label.anchor e')
        self.col = Tix.Control(master, label='Column', variable=self.Column, \
                              min=0, max=100, integer=1, options='entry.width 10 label.width 20 label.anchor e')
        self.len = Tix.Control(master, label='Length of text', variable=self.Length, \
                              min=0, max=100, integer=1, options='entry.width 10 label.width 20 label.anchor e')
        self.bandha = Tix.ComboBox(master, label='Bandha', editable=0, dropdown=1,variable=self.Bandha, \
                              options='entry.width 20 label.width 20 label.anchor e')
        self.plain = Tix.ComboBox(master, label='Plain Text', editable=1, dropdown=1,variable=self.Plain,   \
                              options='entry.width 50 label.width 20 label.anchor e')
        self.bandha.insert(Tix.END,"row by row")
        self.bandha.insert(Tix.END,"mukha bandha")
        self.bandha.insert(Tix.END,"diagonal")

        f = open('Plain.txt') # populate plain text drop down with lines from file
        plain = f.readlines()
        f.close()

        for line in plain:
            self.plain.insert(Tix.END,line[:-1])
        # self.plain.insert(Tix.END,"my name is")
        # self.plain.insert(Tix.END,"anthony gonsalves")
        # self.plain.insert(Tix.END,"main duniya  mein akela hun")

        self.row.grid(row=0, column=1)
        self.col.grid(row=0, column=2)
        self.len.grid(row=0, column=3)
        self.bandha.grid(row=2, column=1)
        self.plain.grid(row=2, column=2)
        return self.e1 # initial focus
    def validate(self):
        try:
            # self.name = self.e1.get()
            self.result = self.Row.get(), self.Column.get(), self.Length.get(), self.Bandha.get(), self.Plain.get()
            return 1
        except ValueError:
            tkMessageBox.showwarning("Invalid input","Illegal values, try again")
            return 0

class chkbx:
    def __init__(self,parent):
        self.v = IntVar()
        self.chk = Checkbutton(parent,variable=self.v)