__author__ = 'naras_mg'

from BaseModel import *
from HideRevealRoutines import *

global grid

def main():
    global grid
    logging.basicConfig(level=logging.DEBUG,filename='Samjna.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    cipherseq=[]
    # hidden_text = 'my name is not very long .. and its not anthony gonsalves'
    # l = len(hidden_text)
    hiding_text = ''

    f = open('Plain.txt')
    plain = f.readlines()
    f.close()
    # print('plain lines')
    # for line in plain: print(line[:-1])
    grid = CellGrid(55,55)

    hide_inplace(grid,grid.rowByrowBandha(xy(0,0)),plain[0][:-1]) #'my name is')
    hide_inplace(grid,grid.mukhaBandha(xy(0,26)),plain[1][:-1]) #'anthony gonsalves')
    hide_inplace(grid,grid.diagonalBandha(xy(32,0)),plain[2][:-1]) #'main duniya  mein akela hun')
    # print reveal(grid,grid.rowByrowBandha(xy(0,0)),25)
    # print reveal(grid,grid.mukhaBandha(xy(0,26)),30)
    # print reveal(grid,grid.diagonalBandha(xy(32,0)),30)
    # print show(grid)
    # print 'cell grid size.. ' + str(grid.size()) +  ' content..\n' + show(grid)

    # print 'cell grid size.. ' + str(grid.size()) +  ' content..\n' + export(grid)

    exportTofile(grid,'export.txt')
    grid = importFromfile('export.txt')
    # print 'cell grid size.. ' + str(grid.size()) +  ' content..\n' + show(grid)
    print reveal(grid,grid.rowByrowBandha(xy(0,0)),25)
    print reveal(grid,grid.mukhaBandha(xy(0,26)),30)
    print reveal(grid,grid.diagonalBandha(xy(32,0)),30)



if __name__ == '__main__':
    main()