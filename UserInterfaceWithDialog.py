from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTextEdit, QLabel, QPushButton, \
    QWidget, QAction,  QSlider, QSpinBox, QHBoxLayout, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem,qApp
# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot

import HideRevealRoutines
from BaseModel import *

import sys,logging
global grid

class MainWindow(QMainWindow):

 def __init__(self, parent=None):

    super(MainWindow, self).__init__(parent)
    self.__grid = None
    self.__labelx = QLabel(self)
    self.__labelx.setText('rows    ')
    self.__spinx = QSpinBox(self)
    self.__spinx.setValue(55)
    self.__sliderx = QSlider(Qt.Horizontal, self)
    self.__sliderx.setValue(55)
    self.__sliderx.setFocusPolicy(Qt.NoFocus)
    self.__sliderx.valueChanged[int].connect(self.changeValueX)
    self.__labely = QLabel(self)
    self.__labely.setText('columns')
    self.startY = QSpinBox(self)
    self.startY.setValue(55)
    self.__slidery = QSlider(Qt.Horizontal, self)
    self.__slidery.setFocusPolicy(Qt.NoFocus)
    self.__slidery.setValue(55)
    self.__slidery.valueChanged[int].connect(self.changeValueY)

    self.__textEdit = QTextEdit()
    # self.__textEdit.setText('blah drone witter agAIn and aGAIN')
    self.setCentralWidget(self.__textEdit)

    f = open('plain.txt')
    plain = f.readlines()
    f.close()
    plain = [s[:-1] for s in plain]
    self.__texts = QComboBox(self)
    self.__texts.addItems(list(plain))
    self.__texts.setCurrentIndex(0)
    self.__texts.currentIndexChanged.connect(self.plaintextSelected)
    self.__textEdit.setText(self.__texts.currentText())

    hboxText = QHBoxLayout()
    hboxText.addWidget(self.__textEdit)

    self.__hboxTexts = QHBoxLayout()
    self.__hboxTexts.addWidget(self.__texts)

    hboxX = QHBoxLayout()
    hboxX.addWidget(self.__labelx)
    hboxX.addWidget(self.__spinx)
    hboxX.addWidget(self.__sliderx)

    hboxY = QHBoxLayout()
    hboxY.addWidget(self.__labely)
    hboxY.addWidget(self.startY)
    hboxY.addWidget(self.__slidery)

    # self.win_widget = WinWidget(self)
    widget = QWidget()
    self.__vlayout = QVBoxLayout(widget)
    self.__vlayout.addLayout(hboxText)
    self.__vlayout.addLayout(self.__hboxTexts)
    self.__vlayout.addLayout(hboxX)
    self.__vlayout.addLayout(hboxY)
    # layout.addWidget(self.win_widget)

    self.setCentralWidget(widget)
    self.statusBar().showMessage('Ready')
    self.toolbar = self.addToolBar('Exit')

    createAction = QAction ('Create', self)
    createAction.setShortcut('Ctrl+Q')
    createAction.setStatusTip('Create a grid(table) of size <rows,columns>')
    createAction.triggered.connect(self.gridCreate)
    self.toolbar = self.addToolBar('Create')
    self.toolbar.addAction(createAction)

    removeAction = QAction('Remove', self)
    removeAction.setShortcut('Ctrl+M')
    removeAction.setStatusTip('Remove created grid')
    removeAction.triggered.connect(self.gridRemove)
    self.toolbar = self.addToolBar('Remove')
    self.toolbar.addAction(removeAction)

    self.__hideAction = QAction ('Hide', self)
    self.__hideAction.setShortcut('Ctrl+Q')
    self.__hideAction.setStatusTip('Hide plain text in grid at <row,column>')
    self.__hideAction.triggered.connect(self.gridHide)
    self.__hideAction.setDisabled(True)
    self.toolbar = self.addToolBar('Hide')
    self.toolbar.addAction(self.__hideAction)

    self.__revealAction = QAction ('Reveal', self)
    self.__revealAction.setShortcut('Ctrl+D')
    self.__revealAction.setStatusTip('Reveal hidden text in grid at <row,column>')
    self.__revealAction.triggered.connect(self.gridReveal)
    self.__revealAction.setDisabled(True)
    self.toolbar = self.addToolBar('Reveal')
    self.toolbar.addAction(self.__revealAction)

    self.__showAction = QAction ('Show', self)
    self.__showAction.setShortcut('Ctrl+W')
    self.__showAction.setStatusTip('Show grid with current content')
    self.__showAction.triggered.connect(self.gridShow)
    self.__showAction.setDisabled(True)
    self.toolbar = self.addToolBar('Show')
    self.toolbar.addAction(self.__showAction)

    helpAction = QAction('Help', self)
    helpAction.setShortcut('Ctrl+P')
    helpAction.setStatusTip('Click a button to create/remove grid, hide/reveal text')
    self.toolbar = self.addToolBar('Help')
    helpAction.triggered.connect(self.callback_help)
    self.toolbar.addAction(helpAction)

    exitAction = QAction ('Exit', self)
    exitAction.setShortcut('Ctrl+Q')
    exitAction.triggered.connect(qApp.quit)
    self.toolbar = self.addToolBar('Exit')
    self.toolbar.addAction(exitAction)

    self.setGeometry(100, 50, 1150, 950)
    self.setWindowTitle('Samjna')
    # self.setWindowIcon (QIcon('logo.png'))
    self.show()
 def callback_help(self):
     self.__textEdit.setText("Create a grid(table) of size <rows,columns>\nRemove a grid\nHide plain text given in grid at <row,col>\nReveal encrypted text at <row,col>")
     # self.statusBar().showMessage("Click a button to create/remove grid, hide/reveal text")

 def changeValueX(self, value):
     self.__spinx.setValue(value)
 def changeValueY(self, value):
     self.startY.setValue(value)
 def createTable(self):
        # Create table
        try:
            r = self.__grid.size().getx()
            c = self.__grid.size().gety()
        except Exception as e:
            print('menu table .. failed .. exception ',e)
            qApp.quit()
        if self.__tableWidget == None:
            self.__tableWidget = QTableWidget(r,c)
            try:
                for i in range(r):
                    for j in range(c):
                        self.__tableWidget.setItem(i, j, QTableWidgetItem(str(self.__grid.get_at(xy(i,j)))))
                self.__vlayout.addWidget(self.__tableWidget)
            except Exception as e:
                print('menu table .. failed .. exception ', e)
 def plaintextSelected(self):
     self.__textEdit.setText(self.__texts.currentText())
 def gridExport(self):
     self.statusBar().showMessage("exported grid size %s", self.__grid.size())
 def gridCreate(self):
     if self.__grid == None:
         colsize = max(int(self.startY.value()),1)
         rowsize = max(int(self.__spinx.value()),1)
         try:
             self.__grid = CellGrid(colsize, rowsize)
         except Exception as ex:
             self.statusBar().showMessage("Create grid failed..", ex)
             self.__grid = None
             return
         message = "created empty grid " + str(self.__grid.size())
         self.__tableWidget = None
         self.createTable()
         self.__hideAction.setEnabled(True)
         self.__showAction.setEnabled(True)
         self.statusBar().showMessage(message)
     else:
         self.statusBar().showMessage("Cancelled ... grid already created")
 def gridRemove(self):
     self.__grid = None
     self.__vlayout.removeWidget(self.__tableWidget)
     self.__tableWidget = None
     self.setLayout(self.__vlayout)
     self.__hideAction.setDisabled(True)
     self.statusBar().showMessage('Grid removed')
 def gridShow(self):
     try:
         r = self.__grid.size().getx()
         c = self.__grid.size().gety()
     except Exception as e:
         qApp.quit()
     try:
         if self.__tableWidget == None:
             self.statusBar().showMessage('menu show .. no grid')
         else:
             for i in range(r):
                 for j in range(c):
                     self.__tableWidget.setItem(i, j, QTableWidgetItem(str(self.__grid.get_at(xy(i, j)))))
     except Exception as e:
         self.statusBar().showMessage('show grid .. failed .. exception ', e)
     # self.statusBar().showMessage("grid size %s", self.__grid.size())
 def gridHide(self):
     global grid
     grid = self.__grid
     dialog = modalHide(self)
     # print(dialog.ok.text())
     if dialog.ok.text()=='Ok':
         # print('if ok yay')
         row = dialog.startX.value()
         col = dialog.startY.value()
         # print('row {} col {} text {}'.format(row,col, dialog.bandha.text()))
         if dialog.bandha.text() == '1-row by row':
             bandhaUsed = self.__grid.rowByrowBandha(xy(row, col))
         elif dialog.bandha.text() == '2-mukhabandha':
             bandhaUsed = self.__grid.mukhaBandha(xy(row, col))
         elif dialog.bandha.text() == '3-diagonal':
             bandhaUsed = self.__grid.diagonalBandha(xy(row, col))
         else:
             self.statusBar().showMessage("Invalid Bandha selection{}".format(dialog.bandha.text()))
             return
         try:
             HideRevealRoutines.hide_inplace(self.__grid, bandhaUsed, self.__textEdit.toPlainText())
         except Exception as ex:
             self.statusBar().showMessage('Failed..' + str(ex))
             return
         # print('Parameters ',self.__grid.lastUsedParameters())
         self.statusBar().showMessage("called hide with parameters: {} text: {}".format(self.__grid.lastUsedParameters(), self.__textEdit.toPlainText()))
         self.__revealAction.setEnabled(True)
     else:
         self.statusBar().showMessage("cancelled")
 def gridReveal(self):
     dialog = modalReveal(self)
     # print(dialog.ok.text())
     if dialog.ok.text()=='Ok':
         # print('if ok yay')
         row = dialog.startX.value()
         col = dialog.startY.value()
         textLength = dialog.length.value()
         # print('row {} col {} text {}'.format(row,col, dialog.bandha.text()))
         if dialog.bandha.text() == '1-row by row':
             bandhaUsed = self.__grid.rowByrowBandha(xy(row, col))
         elif dialog.bandha.text() == '2-mukhabandha':
             bandhaUsed = self.__grid.mukhaBandha(xy(row, col))
         elif dialog.bandha.text() == '3-diagonal':
             bandhaUsed = self.__grid.diagonalBandha(xy(row, col))
         else:
             self.statusBar().showMessage("Invalid Bandha selection {}".format(dialog.bandha.text()))
             return
         try:
             self.__textEdit.setText(HideRevealRoutines.reveal(self.__grid, bandhaUsed,textLength))
         except Exception as ex:
             self.statusBar().showMessage('Failed..' + str(ex))
             return
         self.statusBar().showMessage("called reveal with parameters: {}".format(self.__grid.lastUsedParameters()))
         self.__revealAction.setEnabled(True)
     else:
         self.statusBar().showMessage("cancelled")


class modalHide(QDialog):
    global grid
    def __init__(self, parent):
     super(modalHide, self).__init__(parent)
     okBtn = QPushButton(self)
     okBtn.setText('Ok')
     okBtn.clicked.connect(self.okClicked)
     self.ok = QLabel()
     self.ok.setText('Ok not clicked yet')
     self.__bandhas = QComboBox(self)
     self.__bandhas.addItems(['1-row by row', '2-mukhabandha', '3-diagonal'])
     self.__bandhas.currentIndexChanged.connect(self.bandhaSelected)
     self.bandha = QLabel(self)
     self.bandha.setText('1-row by row')
     self.__lblstartX = QLabel()
     self.__lblstartX.setText('X Start')
     self.__lblstartY = QLabel()
     self.__lblstartY.setText('Y Start')
     self.startX = QSpinBox(self)
     self.startX.setValue(0)
     self.startY = QSpinBox(self)
     self.startY.setValue(0)
     self.__sliderx = QSlider(Qt.Horizontal, self)
     self.__sliderx.setValue(0)
     self.__sliderx.setFocusPolicy(Qt.NoFocus)
     self.__sliderx.valueChanged[int].connect(self.changeValueX)
     self.__slidery = QSlider(Qt.Horizontal, self)
     self.__slidery.setValue(0)
     self.__slidery.setFocusPolicy(Qt.NoFocus)
     self.__slidery.valueChanged[int].connect(self.changeValueY)

     self.createTable()

     self.__hboxX = QHBoxLayout()
     self.__hboxX.addWidget(self.__lblstartX)
     self.__hboxX.addWidget(self.startX)
     self.__hboxX.addWidget(self.__sliderx)

     self.__hboxY = QHBoxLayout()
     self.__hboxY.addWidget(self.__lblstartY)
     self.__hboxY.addWidget(self.startY)
     self.__hboxY.addWidget(self.__slidery)

     self.__hboxTextOk = QHBoxLayout()
     self.__hboxTextOk.addWidget(self.bandha)
     self.__hboxTextOk.addWidget(self.__bandhas)
     self.__hboxTextOk.addWidget(okBtn)
     self.__hboxTextOk.addWidget(self.ok)

     self.__vbox = QVBoxLayout()
     self.__vbox.addLayout(self.__hboxX)
     self.__vbox.addLayout(self.__hboxY)
     self.__vbox.addLayout(self.__hboxTextOk)
     # self.__vbox.addWidget(okBtn)
     self.__vbox.addWidget(self.tableWidget)

     self.setLayout(self.__vbox)
     self.setGeometry(300, 150, 550, 350)
     self.setWindowTitle('Hide plain text where?')
     self.setModal(True)
     self.exec_()
    def bandhaSelected(self):
     self.bandha.setText(self.__bandhas.currentText())
    def changeValueX(self, value):
        self.startX.setValue(value)
    def changeValueY(self, value):
        self.startY.setValue(value)

    def okClicked(self):
     self.ok.setText('Ok')
     # print('ok:', self.ok.text(), 'x:', self.startX.value(), 'y:', self.startY.value())
     self.close()

    def createTable(self):
        # Create table
        try:
            r = grid.size().getx()
            c = grid.size().gety()
        except Exception as e:
            print('create table widget .. failed .. exception ',e)
            qApp.quit()
        self.tableWidget = QTableWidget(r,c)
        try:
            for i in range(r):
                for j in range(c):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(grid.get_at(xy(i,j)))))
        except Exception as e:
            print('failed .. exception ', e)
        # self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class modalReveal(QDialog):
    global grid
    def __init__(self, parent):
     super(modalReveal, self).__init__(parent)
     okBtn = QPushButton(self)
     okBtn.setText('Ok')
     okBtn.clicked.connect(self.okClicked)
     self.ok = QLabel()
     self.ok.setText('Not Ok')
     self.__bandhas = QComboBox(self)
     self.__bandhas.addItems(['1-row by row', '2-mukhabandha', '3-diagonal'])
     self.__bandhas.currentIndexChanged.connect(self.bandhaSelected)
     self.bandha = QLabel(self)
     self.bandha.setText('1-row by row')
     self.__lblstartX = QLabel()
     self.__lblstartX.setText('X Start')
     self.__lblstartY = QLabel()
     self.__lblstartY.setText('Y Start')
     self.startX = QSpinBox(self)
     self.startX.setValue(0)
     self.__sliderx = QSlider(Qt.Horizontal, self)
     self.__sliderx.setValue(0)
     self.__sliderx.setFocusPolicy(Qt.NoFocus)
     self.__sliderx.valueChanged[int].connect(self.changeValueX)
     self.startY = QSpinBox(self)
     self.startY.setValue(0)
     self.__slidery = QSlider(Qt.Horizontal, self)
     self.__slidery.setValue(0)
     self.__slidery.setFocusPolicy(Qt.NoFocus)
     self.__slidery.valueChanged[int].connect(self.changeValueY)
     self.__lbllength = QLabel()
     self.__lbllength.setText('Length')
     self.length = QSpinBox(self)
     self.length.setValue(30)
     self.__sliderLen = QSlider(Qt.Horizontal, self)
     self.__sliderLen.setValue(30)
     self.__sliderLen.setFocusPolicy(Qt.NoFocus)
     self.__sliderLen.valueChanged[int].connect(self.changeValueLength)

     self.createTable()

     self.__hboxX = QHBoxLayout()
     self.__hboxX.addWidget(self.__lblstartX)
     self.__hboxX.addWidget(self.startX)
     self.__hboxX.addWidget(self.__sliderx)

     self.__hboxY = QHBoxLayout()
     self.__hboxY.addWidget(self.__lblstartY)
     self.__hboxY.addWidget(self.startY)
     self.__hboxY.addWidget(self.__slidery)

     self.__hboxLen = QHBoxLayout()
     self.__hboxLen.addWidget(self.__lbllength)
     self.__hboxLen.addWidget(self.length)
     self.__hboxLen.addWidget(self.__sliderLen)
     self.__hboxLen.addWidget(self.ok)

     self.__hboxTextOk = QHBoxLayout()
     self.__hboxTextOk.addWidget(self.bandha)
     self.__hboxTextOk.addWidget(self.__bandhas)
     self.__hboxTextOk.addWidget(okBtn)
     self.__hboxTextOk.addWidget(self.ok)

     self.__vbox = QVBoxLayout()
     self.__vbox.addLayout(self.__hboxX)
     self.__vbox.addLayout(self.__hboxY)
     self.__vbox.addLayout(self.__hboxLen)
     self.__vbox.addLayout(self.__hboxTextOk)
     self.__vbox.addWidget(self.tableWidget)

     self.__vbox.addWidget(okBtn)
     self.setLayout(self.__vbox)
     self.setGeometry(300, 150, 550, 350)
     self.setWindowTitle('Reveal hidden text from where?')
     self.setModal(True)
     self.exec_()

    def createTable(self):
        # Create table
        try:
            r = grid.size().getx()
            c = grid.size().gety()
        except Exception as e:
            print('create table widget .. failed .. exception ',e)
            qApp.quit()
        self.tableWidget = QTableWidget(r,c)
        try:
            for i in range(r):
                for j in range(c):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(grid.get_at(xy(i,j)))))
        except Exception as e:
            print('failed .. exception ', e)
        # self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    def bandhaSelected(self):
     self.bandha.setText(self.__bandhas.currentText())
    def changeValueX(self, value):
        self.startX.setValue(value)
    def changeValueY(self, value):
        self.startY.setValue(value)
    def changeValueLength(self, value):
        self.length.setValue(value)
    def okClicked(self):
     self.ok.setText('Ok')
     # print('ok:', self.ok.text(), 'x:', self.startX.value(), 'y:', self.startY.value())
     self.close()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


def main():
    logging.debug('Session Start')
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,filename='Samjna.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    main()