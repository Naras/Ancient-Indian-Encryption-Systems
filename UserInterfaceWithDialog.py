__author__ = 'naras_mg'
from Tkinter import *
import Tix, tkMessageBox
import DialogGrid,DialogHide,DialogReveal,HideRevealRoutines
from BaseModel import *
import logging

global grid, root, status


def GridCreate():
    global grid,root, status
    if grid!=None:
        status.set("Cancelled ... grid already created")
        return
    d = DialogGrid.Init(root)
    if d.result != None:
        colsize = d.result[0]
        rowsize = d.result[1]
        grid = CellGrid(colsize,rowsize)
        status.set("created empty grid rowsize %s, colsize %s",rowsize, colsize)
        status.puttext(HideRevealRoutines.show(grid))
    else:
        grid = None
        status.set("Cancelled ... no grid created")
def GridRemove():
    global grid,status
    grid = None
    status.set('Grid removed')
def GridShow():
    global grid,root, status
    status.set("grid size %s",grid.size())
    status.puttext(HideRevealRoutines.show(grid))
def GridExport():
    global grid,root, status
    status.set("exported grid size %s",grid.size())
    status.puttext(HideRevealRoutines.export(grid))    # show the exported contents
def GridHide():
    global grid,root, status
    d = DialogHide.Init(root)
    if d.result != None:
        row = int(d.result[0])
        col = int(d.result[1])
        length = int(d.result[2])
        bandha = d.result[3]
        status.puttext( d.result[4])
        if bandha.lower().strip() == 'row by row bandha':BandhaUsed = grid.rowByrowBandha(xy(row,col))
        elif bandha.lower().strip() == 'mukha bandha': BandhaUsed = grid.mukhaBandha(xy(row,col))
        elif bandha.lower().strip() == 'diagonal': BandhaUsed = grid.diagonalBandha(xy(row,col))
        else:
            status.set("%s","Invalid Bandha selection")
            return
        HideRevealRoutines.hide(grid, BandhaUsed,status.gettext()[:-1])
        status.set ("called hide with %s", d.result)
    else: status.set ("%s","cancelled")
def GridReveal():
    global grid,root, status
    d = DialogReveal.Init(root)
    if d.result != None:
        row = int(d.result[0])
        col = int(d.result[1])
        length = int(d.result[2])
        bandha = d.result[3]
        if bandha.lower().strip() == 'row by row bandha':BandhaUsed = grid.rowByrowBandha(xy(row,col))
        elif bandha.lower().strip() == 'mukha bandha': BandhaUsed = grid.mukhaBandha(xy(row,col))
        elif bandha.lower().strip() == 'diagonal': BandhaUsed = grid.diagonalBandha(xy(row,col))
        else:
            status.set("%s","Invalid Bandha selection")
            return
        revealed = HideRevealRoutines.reveal(grid, BandhaUsed,length)
        status.set ("called reveal with %s", d.result)
        status.puttext(revealed)
    else: status.set ("%s","cancelled")
def GridExportToFile():
    global grid,root, status
    HideRevealRoutines.exportTofile(grid,'export.txt')
    status.set("exported grid size %s to file export.txt",grid.size())
def GridImportFromFile():
    global grid,root, status
    grid = HideRevealRoutines.importFromfile('export.txt')
    status.set("imported grid size %s from file export.txt",grid.size())
def HelpAbout():
    status.set("Help, I need somebody! Not just anybody. You know I need someone. Heeeellllppp!")
def QuitApp():
    # if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()
class StatusBar(Frame):
    __txtarea = None
    __t = None
    def __init__(self, master):
        Frame.__init__(self, master)
        self.createtext()
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()
    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
        frame = Frame(Frame)
    '''
    def callbackKey(self, event):
        strng = "Key at " + str(event.x) + "," + str(event.y) + "is -->" + str(event.keycode) + "(" + str(event.keysym) + ")"
        self.set("%20s",strng)
    def callbackMousemove(self, event):
        strng = "Mouse at " + str(event.x) + "," + str(event.y)
        self.set("%20s",strng)
        '''
    def createtext(self):
        # create a Text area
        self.__txtarea = Frame(self)
        self.__t = Text(self.__txtarea)
        self.__t.pack(side=TOP)
        self.__t.insert(END,"this area will show  grid content - once the grid is created")
        # self.__t.bind("<Key>", self.callbackKey)
        # self.__t.bind("<Button-1>", self.callbackKey)
        self.__txtarea.pack()
        win = Tix.ScrolledText(self.__txtarea, scrollbar='auto')

    def gettext(self):
        return self.__t.get("1.0",END) #'end-1c')
    def puttext(self,txt):
        self.__t.delete("1.0",END)
        self.__t.insert(END,txt)
def main():
    global grid,root, status
    grid = None
    logging.basicConfig(level=logging.DEBUG,filename='Samjna.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    root = Tix.Tk()
    # create a menu
    menu = Menu(root)
    root.config(menu=menu)

    gridmenu = Menu(menu)
    menu.add_cascade(label="Grid", menu=gridmenu)
    gridmenu.add_command(label="Create", command=GridCreate)
    gridmenu.add_command(label="Show", command=GridShow)
    gridmenu.add_command(label="Remove", command=GridRemove)
    gridmenu.add_command(label="Exit", command=QuitApp)

    hiderevealmenu = Menu(menu)
    menu.add_cascade(label="Hide/Reveal", menu=hiderevealmenu)
    hiderevealmenu.add_command(label="Hide", command=GridHide)
    hiderevealmenu.add_command(label="Reveal", command=GridReveal)

    eximmenu = Menu(menu)
    menu.add_cascade(label="Export/Import", menu=eximmenu)
    eximmenu.add_command(label="Export", command=GridExport)
    eximmenu.add_command(label="Export to file", command=GridExportToFile)
    eximmenu.add_command(label="Import from file", command=GridImportFromFile)

    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=HelpAbout)

    # create a statusbar
    status = StatusBar(root)
    status.pack(side=BOTTOM, fill=X)
    status.set("Blank already:-)")

    root.mainloop()



if __name__ == '__main__':
    main()
