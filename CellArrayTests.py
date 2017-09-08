__author__ = 'naras_mg'
from BaseModel import *

# a cell array, with message insertion & hide/reveal operations .. just an extra option .. usually we will use cell grids

#  cell sequence generation .. sample routines and usage

global m,n
m = 3
n = 2

def delta1():
    while True:
        # yield 1
        yield m
def delta2():
    while True:
        # yield 1
        yield n
def numbers(start, deltas, max):
    i = start
    while i <= max:
        yield i
        i += next(deltas)

noof_cells = 113
CA = CellArray([Cell()] * noof_cells)  # a column of b cells
# print(CA.size())
cipherseq=[]
hidden_text = 'my name is not very long, and its not anthony gonsalves'
l = len(hidden_text)
hiding_text = ''

for (x,z) in zip((numbers(1, delta1(), l * m)),range(l)):
    cipherseq.append(x)
    c = hidden_text[z]
    CA.insert_at(Cell(c),x)
    hiding_text+=str(CA.get_at(x))
print 'hiding ->' + hiding_text

plain_text = ''
plainseq = []
for x in (numbers(1, delta1(), l * m)):
    plainseq.append(x)
    plain_text += str(CA.get_at(x))

'''print('hider sequence')
print(cipherseq)
print('revealer sequence')
print(plainseq)
print('revealing ->' + plain_text)'''

s = ''
for cel in CA.generator():
    if cel.isEmpty(): s += '.'
    else: s += cel.get()
print 'cell array size.. ' + str(CA.size()) +  ' content..\n' + s
CA.fillRandomNulls()
s=''
for cel in CA.generator():
    if cel.isEmpty(): s += '.'
    else: s += cel.get()
print 'cell array size.. ' + str(CA.size()) +  ' ..\n' + s
