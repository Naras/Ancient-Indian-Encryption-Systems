__author__ = 'naras_mg'

from BaseModel import *
from HideRevealRoutines import *

global grid

def main():
    global grid
    logging.basicConfig(level=logging.DEBUG,filename='Samjna.log',format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    f = open('Plain.txt')
    plain = f.readlines()
    f.close()
    r,c = 62,55
    grid = CellGrid(r,c)
    rowByrow = it_fits_in(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])
    if rowByrow: hide_inplace(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])  # )'my name is'
    mukha =  it_fits_in(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])
    if mukha: hide_inplace(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])  # 'anthony gonsalves')
    diagonal = it_fits_in(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])
    if diagonal: hide_inplace(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])  # 'main duniya  mein akela hun')
    if rowByrow: print('after hide .. revealing ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
    if mukha: print(reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
    if diagonal: print(reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))

    exportTofile(grid,'export.txt')
    grid = importFromfile('export.txt')
    if rowByrow: print('after import .. revealing ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
    if mukha: print(reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
    if diagonal: print(reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))

    exportTofile(grid,'exportNoSizeInfo.txt',include_size=False)
    grid = importFromfile('exportNoSizeInfo.txt',size=(r,c))
    if rowByrow: print('after import w/size .. revealing ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
    if mukha: print(reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
    if diagonal: print(reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))


if __name__ == '__main__':
    main()