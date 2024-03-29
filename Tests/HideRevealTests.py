__author__ = 'naras_mg'

from Source.Model.HideRevealRoutines import *
import codecs
global grid

def main():
    global grid
    logging.basicConfig(level=logging.DEBUG, filename='EncryptionTests.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    f = codecs.open('../Source/Plain_IndianLanguages_Unicode.txt',encoding='utf-8')
    # f = open('../Source/Plain.txt')
    plain = f.readlines()
    f.close()
    # for line in plain: print(len(line[:-1]))
    r,c = 92,75
    grid = CellGrid(r,c)
    rowByrow = it_fits_in(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])
    if rowByrow: hide_inplace(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])  # )'my name is'
    mukha = it_fits_in(grid, grid.mukhaBandha(xy(33, 0)), plain[1][:-1])
    if mukha: hide_inplace(grid, grid.mukhaBandha(xy(33, 0)), plain[1][:-1])  # 'anthony gonsalves')
    diagonal = it_fits_in(grid, grid.diagonalBandha(xy(0, 44)), plain[2][:-1])
    if diagonal: hide_inplace(grid, grid.diagonalBandha(xy(0, 44)), plain[2][:-1])  # 'main duniya  mein akela hun')
    print('rowbyrow %s mukha %s diagonal %s'%(rowByrow, mukha, diagonal))
    if rowByrow: print('after hide .. revealing rowbyrow.. ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), len(plain[0][:-1])))
    if mukha: print('mukha.. %s'%reveal(grid, grid.mukhaBandha(xy(33, 0)), len(plain[1][:-1])))
    if diagonal: print('diagonal.. %s'%reveal(grid, grid.diagonalBandha(xy(0, 44)), len(plain[2][:-1])))
    exportTofile(grid,'export.txt')
    grid = importFromfile('export.txt')
    if rowByrow: print('after import .. revealing ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), len(plain[0][:-1])))
    if mukha: print('mukha.. %s'%reveal(grid, grid.mukhaBandha(xy(33, 0)), len(plain[1][:-1])))
    if diagonal: print('diagonal.. %s'%reveal(grid, grid.diagonalBandha(xy(0, 44)), len(plain[2][:-1])))

    exportTofile(grid,'exportNoSizeInfo.txt',include_size=False)
    grid = importFromfile('exportNoSizeInfo.txt',size=(r,c))
    if rowByrow: print('after import w/size .. revealing ', reveal(grid, grid.rowByrowBandha(xy(0, 0)), len(plain[0][:-1])))
    if mukha: print(reveal(grid, grid.mukhaBandha(xy(33, 0)), len(plain[1][:-1])))
    if diagonal: print(reveal(grid, grid.diagonalBandha(xy(0, 44)), len(plain[2][:-1])))
'''
    sineX, sineY, cosineX, cosineY, heartX, heartY = 4, 8, 12, 20, 45, 45
    sine = it_fits_in(grid, grid.sineBandha(xy(sineX, sineY)), plain[1][:-1])
    if sine: hide_inplace(grid, grid.sineBandha(xy(sineX, sineY)), plain[1][:-1])  # 'main duniya  mein akela hun')
    cosine = it_fits_in(grid, grid.cosineBandha(xy(cosineX, cosineY)), plain[0][:-1])
    if cosine: hide_inplace(grid, grid.cosineBandha(xy(cosineX, cosineY)), plain[0][:-1])  # 'main duniya  mein akela hun')
    heart = it_fits_in(grid, grid.cosineBandha(xy(heartX, heartY)), plain[2][:-1])
    if heart: hide_inplace(grid, grid.heartBandha(xy(heartX, heartY)), plain[2][:-1])  # 'main duniya  mein akela hun')
    print('sine %s cosine %s heart %s' % (sine, cosine, heart))
    if sine: print('sine.. %s'%reveal(grid, grid.sineBandha(xy(sineX, sineY)), len(plain[1][:-1])))
    if cosine: print('cosine.. %s'%reveal(grid, grid.cosineBandha(xy(cosineX, cosineY)), len(plain[0][:-1])))
    if heart: print('heart.. %s'%reveal(grid, grid.heartBandha(xy(heartX, heartY)), len(plain[2][:-1])))
'''

if __name__ == '__main__':
    main()