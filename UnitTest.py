__author__ = 'naras_mg'
from BaseModel import *

# Basic tests:
# 1. Create and manipulate cells
samp = Cell(None)
samp.set('setted')
print 'samp ' + str(samp.size()) + '..' + str(samp)

# 2. Create and manipulate Cell Arrays
CA = CellArray([Cell('one'),Cell(2),Cell('four')])
CA.append([Cell(5),Cell('six')])
CA.insert_at([Cell(33),Cell('thirtythree')],3)
# CA.get_at(2).clear()
CA.modify_at([Cell('many'),Cell('notmany')],1)
CA.remove([Cell('four'),Cell(5)])
CA.remove_at(5)

# print cell array content
s=''
for ss in CA.generator():
    s += str(ss) + '(size ' + str(ss.size()) +  '),'
print('\npre-finally..cell array size ' + str(CA.size()) + '\ncontent..' + s[:-1])

#3. create and manipulate Cell Grid
CG = CellGrid(2,3,[Cell('one'),Cell(2),Cell('four')])
# CG.insert_at([Cell('new'),Cell('one more')],xy(0,2))
# print('at 1,2 .. ' + str(CG.get_at(xy(1,1)))  + '  size ' + str(CG.get_at(xy(1,1)).size()))
CG.modify_at([Cell('last-but-one'),Cell('last')],xy(1,2))
CG.remove_at(xy(2,2))

cg_as_string,i = '',0
# print Cell Grid content, each row in a line
for cel in CG.get().generator():
    if i >= CG.size().getx() - 1:
        i = 0
        separator = '\n'
    else:
        i += 1
        separator = ','
    cg_as_string += str(cel) + '(size ' + str(cel.size()) +  ')' + separator
print('\nfinally..cell grid size.. ' + str(CG.size()) +  ' content..\n' + cg_as_string[:-1])

print ('diagonal Bandha..')
for xy in CG.diagonalBandha(): print(xy)
print ('rowByrow Bandha..')
for xy in CG.rowByrowBandha(): print(xy)
print ('mukha Bandha..')
for xy in CG.mukhaBandha(): print(xy)
