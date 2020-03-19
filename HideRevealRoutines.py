__author__ = 'naras_mg'
from BaseModel import *
import logging

def hide(grid,bandha,text):
    # hiding_text = ''
    cipherseq=[]
    if len(text) > grid.size().getx() * grid.size().gety(): logging.warning('text to hide longer than available size')
    for (xy,z) in zip(bandha,range(len(text))):
        cipherseq.append(xy)
        c = text[z]
        grid.insert_at(Cell(c),xy)
        # logging.debug('size now..' + str(grid.size()))
        # hiding_text += str(grid.get_at(xy))
    # print(str(len(text)) + '-' + hiding_text)
    s=''
    for xy in cipherseq: s += str(xy)
    logging.info('Parameters %s hider sequence %s',grid.lastUsedParameters(),s)
    # logging.info('Parameters %s',grid.lastUsedParameters())
def hide_inplace(grid,bandha,text):
    cipherseq=[]
    for (xy,z) in zip(bandha,range(len(text))):
        cipherseq.append(xy)
        c = text[z]
        grid.modify_at(Cell(c),xy)
    s=''
    for xy in cipherseq: s += str(xy)
    logging.info('Parameters %s hider sequence %s',grid.lastUsedParameters(),s)
def reveal(grid,bandha,len_text):
    plain_text = ''
    # plainseq = []
    for (xy,z) in zip(bandha,range(len_text)):
        # plainseq.append(xy)
        plain_text += str(grid.get_at(xy))
    # s=''
    # for xy in plainseq: s+=str(xy)
    # logging.info('Bandha %s revealer sequence %s',grid.lastUsedBandha(),s)
    return plain_text
def export(grid):
    grid.get().fillRandomNulls()
    logging.info('exported grid size %s',str(grid.size()))
    return show(grid)
def show(grid):
    grid_string,i = '',0
    for cel in grid.get().generator():
        if i >= grid.size().getx() - 1:
            i = 0
            separator = '\n'
        else:
            i += 1
            separator = ''
        if cel.isEmpty():
            cel = '.'
        # else:
        grid_string += str(cel) + separator
    return grid_string
def exportTofile(grid,file,include_size=True):
    grid.get().fillRandomNulls()
    grid_string = ''
    for cel in grid.get().generator():
        grid_string += str(cel)
    f = open(file,'w')
    if include_size: f.write(str(grid.size())+'\n')
    f.write(grid_string)    # write the grid contents to file
    f.close()
    logging.info('exported to file - ' + file + '.. grid size %s',str(grid.size()))
    return 0
def importFromfile(file,size=None):
    f = open(file)
    if size==None:
        size = f.readline()
        comma = size.index(',')
        rowsize = int(size[1:comma])
        colsize = int(size[comma+1:-2])
        grid = CellGrid(colsize,rowsize)
    else:
        colsize,rowsize=size
        grid = CellGrid(colsize,rowsize)
    grid_string = f.readline()
    # print(grid_string)
    x,y = 0,0
    for c in grid_string:
        grid.modify_at(Cell(c),xy(x,y))
        y += 1
        if y >= rowsize:
            y = 0
            x += 1
    return grid

