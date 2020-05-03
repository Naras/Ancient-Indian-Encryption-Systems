from unittest import TestCase
from Source.Model.HideRevealRoutines import *
import os
class Test(TestCase):
    def setUp(self):
        global grid, plain, rows, cols
        f = open('../Source/Plain.txt')
        plain = f.readlines()
        f.close()
        rows, cols = 62, 55
        grid = CellGrid(rows, cols)
        logging.basicConfig(level=logging.DEBUG, filename='EncryptionTests.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    def test_it_fits_in(self):
        global grid, plain
        self.assertEqual(True, it_fits_in(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1]))
        self.assertEqual(True, it_fits_in(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1]))
        self.assertEqual(True, it_fits_in(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1]))

    def test_hide_reveal(self):
        global grid, plain
        rowByrow = it_fits_in(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])
        if rowByrow: hide_inplace(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])  # )'my name is'
        mukha = it_fits_in(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])
        if mukha: hide_inplace(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])  # 'anthony gonsalves')
        diagonal = it_fits_in(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])
        if diagonal: hide_inplace(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])  # 'main duniya  mein akela hun')
        if rowByrow: self.assertEqual(plain[0][:-1], reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
        if mukha: self.assertEqual(plain[1][:-1], reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
        if diagonal: self.assertEqual(plain[2][:-1], reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))

    def test_import_fromfile(self):
        global grid, plain, rows, cols
        rowByrow = it_fits_in(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])
        if rowByrow: hide_inplace(grid, grid.rowByrowBandha(xy(0, 0)), plain[0][:-1])  # )'my name is'
        mukha = it_fits_in(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])
        if mukha: hide_inplace(grid, grid.mukhaBandha(xy(26, 0)), plain[1][:-1])  # 'anthony gonsalves')
        diagonal = it_fits_in(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])
        if diagonal: hide_inplace(grid, grid.diagonalBandha(xy(0, 32)), plain[2][:-1])  # 'main duniya  mein akela hun')
        exportTofile(grid, 'export.txt')
        grid = importFromfile('export.txt')
        if rowByrow: self.assertEqual(plain[0][:-1], reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
        if mukha: self.assertEqual(plain[1][:-1], reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
        if diagonal: self.assertEqual(plain[2][:-1], reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))
        exportTofile(grid, 'export.txt', include_size=False)
        grid = importFromfile('export.txt', size=(rows, cols))
        if rowByrow: self.assertEqual(plain[0][:-1], reveal(grid, grid.rowByrowBandha(xy(0, 0)), 25))
        if mukha: self.assertEqual(plain[1][:-1], reveal(grid, grid.mukhaBandha(xy(26, 0)), 30))
        if diagonal: self.assertEqual(plain[2][:-1], reveal(grid, grid.diagonalBandha(xy(0, 32)), 30))
        os.remove('export.txt')
        # os.remove('EncryptionTests.log')

