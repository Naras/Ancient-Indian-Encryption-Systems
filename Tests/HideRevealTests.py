__author__ = 'naras_mg'

from Source.Model.HideRevealRoutines import *
import codecs
global grid

def main():
    global grid
    logging.basicConfig(level=logging.DEBUG, filename='EncryptionTests.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    # f = codecs.open('../Source/Plain_IndianLanguages_Unicode.txt',encoding='utf-8')
    f = open('../Source/Plain.txt')
    plain = [line[:-1] for line in f.readlines()]
    f.close()
    # for line in plain: print(len(line), line)
    r, c = 62, 55  # 92, 75
    grid = CellGrid(r, c)
    bandhasFit, bandhas, xys = [], [grid.rowByrowBandha, grid.mukhaBandha, grid.diagonalBandha], [xy(0, 0), xy(26, 0), xy(0, 31)]
    for bandha_xy_plaintext in zip(bandhas, xys, plain):
        bandha, x_y, plaintext = bandha_xy_plaintext
        bandhaFits = it_fits_in(grid, bandha(x_y), plaintext)
        bandhasFit.append(bandhaFits)
        if bandhaFits: hide_inplace(grid, bandha(x_y), plaintext)
    bandhasPossible = ['rowbyrow', 'mukha', 'diagonal']
    print('bandhas possible %s' % [s[0] for s in zip(['rowbyrow', 'mukha', 'diagonal'], bandhasFit) if s[1]])
    for i, bandha_xy_plaintext_fits in enumerate(zip(bandhas, xys, plain, bandhasFit)):
        bandha, x_y, plaintext, bandhaFits = bandha_xy_plaintext_fits
        if bandhaFits: print('revealing bandha: %s text: "%s"'%(bandhasPossible[i], reveal(grid, bandha(x_y), len(plaintext))))

    exportTofile(grid, 'export.txt')
    grid = importFromfile('export.txt')
    for i, bandha_xy_plaintext_fits in enumerate(zip(bandhas, xys, plain, bandhasFit)):
        bandha, x_y, plaintext, bandhaFits = bandha_xy_plaintext_fits
        if bandhaFits: print('after import .. revealing bandha: %s text: "%s"'%(bandhasPossible[i], reveal(grid, bandha(x_y), len(plaintext))))

    exportTofile(grid,'exportNoSizeInfo.txt', include_size=False)
    grid = importFromfile('exportNoSizeInfo.txt', size=(r,c))
    for i, bandha_xy_plaintext_fits in enumerate(zip(bandhas, xys, plain, bandhasFit)):
        bandha, x_y, plaintext, bandhaFits = bandha_xy_plaintext_fits
        if bandhaFits: print('after export no size/import ..revealing bandha: %s text: "%s"'%(bandhasPossible[i], reveal(grid, bandha(x_y), len(plaintext))))

'''
    r, c = 99, 99
    grid = CellGrid(r, c)
    sineX, sineY, cosineX, cosineY, heartX, heartY = 45, 35, 12, 20, 50, 50
    sine = it_fits_in(grid, grid.sineBandha(xy(sineX, sineY)), plain[1])
    if sine: hide_inplace(grid, grid.sineBandha(xy(sineX, sineY)), plain[1])  # 'main duniya  mein akela hun')
    cosine = it_fits_in(grid, grid.cosineBandha(xy(cosineX, cosineY)), plain[0])
    if cosine: hide_inplace(grid, grid.cosineBandha(xy(cosineX, cosineY)), plain[0])  # 'main duniya  mein akela hun')
    heart = it_fits_in(grid, grid.cosineBandha(xy(heartX, heartY)), plain[2])
    if heart: hide_inplace(grid, grid.heartBandha(xy(heartX, heartY)), plain[2])  # 'main duniya  mein akela hun')
    print('sine %s cosine %s heart %s' % (sine, cosine, heart))
    if sine: print('sine.. %s'%reveal(grid, grid.sineBandha(xy(sineX, sineY)), len(plain[1])))
    if cosine: print('cosine.. %s'%reveal(grid, grid.cosineBandha(xy(cosineX, cosineY)), len(plain[0])))
    if heart: print('heart.. %s'%reveal(grid, grid.heartBandha(xy(heartX, heartY)), len(plain[2])))
'''

if __name__ == '__main__':
    main()