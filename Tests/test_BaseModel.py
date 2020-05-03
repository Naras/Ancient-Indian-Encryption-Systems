from unittest import TestCase
from Source.Model.BaseModel import *

class TestCell(TestCase):
    def test_cell(self):
        # 1. Create and manipulate cells
        samp = Cell(None)
        samp.set('setted')
        # print('samp ' + str(samp.size()) + '..' + str(samp))
        self.assertEqual(samp.get(), 'setted')
        self.assertEqual(samp.size(), 6)

    def test_clear(self):
        pass

    def test_is_empty(self):
        pass
class TestCellArray(TestCase):
    def test_cellArray(self):
        # 2. Create and manipulate Cell Arrays
        CA = CellArray([Cell('one'), Cell(2), Cell('four')])
        self.assertEqual(CA.size(), 3)
        self.assertEqual(CA.get_at(0).get(), 'one')
        self.assertEqual(CA.get_at(1).get(), 2)
        self.assertEqual(CA.get_at(2).get(), 'four')
        CA.append([Cell(5), Cell('six')])
        # print(cellArrayContent(CA))
        self.assertEqual(cellArrayContent(CA), {'content': ['one', '2', 'four', '5', 'six'], 'size': 5})
        self.assertEqual(CA.size(), 5)
        self.assertEqual(CA.get_at(3).get(), 5)
        self.assertEqual(CA.get_at(4).get(), 'six')
        CA.insert_at([Cell(33), Cell('thirtythree')], 3)
        # print(cellArrayContent(CA))
        self.assertEqual(cellArrayContent(CA),
                         {'content': ['one', '2', 'four', '33', 'thirtythree', '5', 'six'], 'size': 7})
        self.assertEqual(CA.size(), 7)
        self.assertEqual(CA.get_at(3).get(), 33)
        self.assertEqual(CA.get_at(4).get(), 'thirtythree')
        self.assertEqual(CA.get_at(5).get(), 5)
        self.assertEqual(CA.get_at(6).get(), 'six')
        # CA.get_at(2).clear()
        CA.modify_at([Cell('many'), Cell('notmany')], 1)
        # print(cellArrayContent(CA))
        self.assertEqual(cellArrayContent(CA),
                         {'content': ['one', 'many', 'notmany', 'four', '33', 'thirtythree', '5', 'six'], 'size': 8})
        self.assertEqual(CA.size(), 8)
        self.assertEqual(CA.get_at(1).get(), 'many')
        self.assertEqual(CA.get_at(2).get(), 'notmany')
        CA.remove([Cell('four'), Cell(5)])
        self.assertEqual(CA.size(), 6)
        # print(cellArrayContent(CA))
        self.assertEqual(cellArrayContent(CA),
                         {'content': ['one', 'many', 'notmany', '33', 'thirtythree', 'six'], 'size': 6})
        self.assertEqual(CA.get_at(5).get(), 'six')
        CA.remove_at(5)
        self.assertEqual(CA.size(), 5)
        # print(cellArrayContent(CA))
        self.assertEqual(cellArrayContent(CA), {'content': ['one', 'many', 'notmany', '33', 'thirtythree'], 'size': 5})
        self.assertEqual(CA.get_at(4).get(), 'thirtythree')
class TestCellGrid(TestCase):
    def test_cellGrid(self):
        # 3. create and manipulate Cell Grid
        CG = CellGrid(2, 3, [Cell('one'), Cell(2), Cell('four')])
        self.assertEqual(cellgridContent_byiterator(CG),
                         {'content': [['one', '2', 'four'],
                                      ['<null>', '<null>', '<null>']], 'size': '(3,2)'})
        CG.insert_at([Cell('new'), Cell('one more')], xy(0, 1))
        # print(cellgridContent_byiterator(CG))
        self.assertEqual('new', str(CG.get_at(xy(0, 1))))
        self.assertEqual(3, CG.get_at(xy(0, 1)).size())
        self.assertEqual( 'one more', str(CG.get_at(xy(1, 1))))
        self.assertEqual(8, CG.get_at(xy(1, 1)).size())
        try:
            self.assertEqual(0, xy('na', 'na'))
        except TypeError as e:
            self.assertEqual("invalid argument types..(<class 'str'>,<class 'str'>", str(e))
        try:
            self.assertEqual('one more', str(CG.get_at(xy(0, 3))))
        except IndexError as e:
            self.assertEqual('Index error x,y (0,3) size (3,3) content:one,2,four,new,one more,<null>,<null>,<null>,<null>', str(e))
        # print(cellArrayContent(CG.get()))
        # print(cellgridContent_bygenerator(CG))
        # print(cellgridContent_byiterator(CG))
        self.assertEqual({'content': [['one', '2', 'four'],
                                      ['new', 'one more', '<null>'],
                                      ['<null>', '<null>', '<null>']], 'size': '(3,3)'}, cellgridContent_byiterator(CG))
        CG.modify_at([Cell('last-but-one'), Cell('last')], xy(1, 2))
        self.assertEqual('last-but-one', str(CG.get_at(xy(1, 2))))
        self.assertEqual(12, CG.get_at(xy(1, 2)).size())
        self.assertEqual({'content': [['one', '2', 'four'],
                                      ['new', 'one more', '<null>'],
                                      ['<null>', 'last-but-one', 'last'],
                                      ['<null>', '<null>', '<null>']], 'size': '(3,4)'}, cellgridContent_byiterator(CG))
        CG.remove_at(xy(1, 2))  # last-but-one
        self.assertEqual(cellgridContent_byiterator(CG),
                         {'content': [['one', '2', 'four'],
                                      ['new', 'one more', '<null>'],
                                      ['<null>', 'last', '<null>'],
                                      ['<null>', '<null>', '<null>']], 'size': '(3,4)'})
        CG.remove_at(xy(2, 0))  # four
        self.assertEqual({'content': [['one', '2', 'new'],
                                      ['one more', '<null>', '<null>'],
                                      ['last', '<null>','<null>'],
                                      ['<null>', '<null>', '<null>']], 'size': '(3,4)'}
                        , cellgridContent_byiterator(CG))
        self.assertEqual(bandhaPath(CG.diagonalBandha()), '(0,0)(1,1)(2,2)')
        self.assertEqual(bandhaPath(CG.rowByrowBandha()),
                         '(0,0)(1,0)(2,0)(0,1)(1,1)(2,1)(0,2)(1,2)(2,2)(0,3)(1,3)(2,3)')
        self.assertEqual(bandhaPath(CG.mukhaBandha()), '(0,0)(0,1)(0,2)(0,3)(1,0)(1,1)(1,2)(1,3)(2,0)(2,1)(2,2)(2,3)')

def bandhaPath(bandha):
    s = ''
    for xy in bandha: s += str(xy)
    return s
def cellArrayContent(CA):
    s = []
    for ss in CA.get():
        s += [str(ss)]
    return {'size': CA.size(), 'content': s}
def cellgridContent_byiterator(CG):
    cg, cg_row, i = [], [], 0
    # convert Cell Grid to list of rows, each row a list
    it = iter(CG)
    for r, c, cel in it:
        if r > 0 and c == 0:
            cg += [cg_row]
            cg_row = [str(cel)]
        else:
            cg_row += [str(cel)]
    cg += [cg_row]
    return {'size': str(CG.size()), 'content': cg}

'''
def cellgridContent_bygenerator(CG):
    cg,cg_row,i = [],[],0
    # print(Cell Grid content, each row in a line)
    for cel in CG.generator():
        if i > CG.size().getx():
            i = 0
            cg += [cg_row]
            cg_row = []
        else:
            i += 1
            cg_row += [str(cel)]
    return cg
'''
