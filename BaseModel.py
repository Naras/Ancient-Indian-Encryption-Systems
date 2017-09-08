__author__ = 'naras_mg'

import string, random, array
# import logging

class Cell:
    "a 2D table consists of cells"
    __content = None
    __empty = True
    def __init__(self,value=None):
        if not value is None:
            self.__content = value
            self.__empty = False
        else:
            self.__empty = True
    def get(self):
        return self.__content
    def set(self,value):
        self.__content = value
        self.__empty = False
    def size(self):
        if self.__empty:
            return 0
        elif isinstance(self.__content,int):
            return len(str(self.__content).strip())
        else:
            return len(self.__content)
    def clear(self):
        self.__content=None
        self.__empty = True
    def isEmpty(self):
        return self.__empty
    def __repr__(self):
        return self.__content
    def __str__(self):
        if self.__empty:
            return('<null>')
        else:
            return str(self.__content)
    def __eq__(self, other):
        if self.__content == other:
            return True
        else:
            return False
    # def fillRandomChar(self):
    #     if self.__empty:
    #         self.__content = random.SystemRandom().choice(string.ascii_letters)
    #         self.__empty = False
class CellArray:
    " a cell array is a list of cells"
    __content = None
    __empty = True
    __cellsEmpty = True
    def __init__(self,*args):
        self.__content=[]
        for arg in args:
            if isinstance(arg,list):
                for item in arg:
                    if isinstance(item, Cell):
                        self.__content.append(item)
                    else:
                        raise TypeError('list item should be a Cell, but is..' + str(type(item)))
            elif isinstance(arg,Cell):
                self.__content.append(arg)
            elif arg == None:
                pass
            else:
                raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
        self.__empty = False
        self.__cellsEmpty = False
    def get(self):
        return self.__content
    def size(self):
        if self.__empty:
            return 0
        else:
            return len(self.__content)
    def get_at(self,index):
        return self.__content[index]
    def remove_at(self,index):
        if index in range(self.size()):
            del self.__content[index]
        else:
            raise IndexError('Index ' + str(index) + ' out of bounds 0..' + str(self.size()) )
    def append(self,arg):  # append another cell or list of cells
        if isinstance(arg,list):
           for item in arg:
            if isinstance(item, Cell):
                self.__content.append(item)
            else:
                raise TypeError('list item  should be a Cell, but is..' + str(type(item)))
        elif isinstance(arg, Cell):
            self.__content.append(arg)
        else:
            raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
    def insert_at(self,arg,index):  # insert a cell or a list of cells in a particular position
        if isinstance(arg,list):
         for item in arg:
            if isinstance(item,Cell):
                if index in range(self.size()):
                     self.__content.insert(index,item)
                else:
                    self.__content.append(item)
                    # raise IndexError('Index ' + str(index) + ' out of bounds 0..' + str(self.size()) )
                index += 1
            else:
                raise TypeError('list item should be a Cell, but is..' + str(type(item)))
        elif isinstance(arg, Cell):
            if index in range(self.size()):
                self.__content.insert(index,arg)
            else:
                self.__content.append(arg)
                # raise IndexError('Index ' + str(index) + ' out of bounds 0..' + str(self.size()) )
        else:
            raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
    def remove(self,arg):  # remove a cell or a list of cells ?!
        if isinstance(arg,list):
           for item in arg:
            if isinstance(item, Cell):
                self.__content.remove(item)
            else:
                raise TypeError('list item  should be a Cell, but is..' + str(type(item)))
        elif isinstance(arg, Cell):
            self.__content.remove(arg)
        else:
            raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
    def modify_at(self,arg,index):  # modify a cell in a particular position
        if isinstance(arg,list):
            if index in range(self.size()):
                self.__content[index]=arg[0]
                index += 1
                for item in arg[1:]:
                 self.__content.insert(index,item)
                 index += 1
            else:
                raise IndexError('Index ' + str(index) + ' out of bounds 0..' + str(self.size()) )
        elif isinstance(arg, Cell):
            if index in range(self.size()):
                self.__content[index] = arg
            else:
                raise IndexError('Index ' + str(index) + ' out of bounds 0..' + str(self.size()) )
        else:
            raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
    def isEmpty(self):
        return self.__empty
    def allCellsEmpty(self):
        self.__empty = False
        for cell in self.__content:
            self.__empty = self.__empty | cell.isEmpty()
        return self.__empty
    def clear(self):
        self.__content = None
        self.__empty = True
    def clearAll(self):
        for cell in self.__content:
            cell.clear()
        self.__cellsEmpty = True
        self.__empty = False
    def generator(self):
        for index in range(len(self.__content)):
            yield(self.__content[index])
    # def __repr__(self):
    #     return self.content
    def __str__(self):
        return ''.join(str(self.__content))
    def fillRandomNulls(self):
        s = string.ascii_letters + string.digits
        for index in range(len(self.__content)):
            if self.__content[index].isEmpty():
                self.modify_at(Cell(random.choice(s)),index)
class xy:
    __x = None
    __y = None
    def __init__(self,x,y):
      if isinstance(x,int) and isinstance(y,int):
        self.__x = x
        self.__y = y
      else:
          raise TypeError( 'invalid argument types..(' + str(type(x)) + ',' + str(type(y)))
    def getx(self): return self.__x
    def gety(self): return self.__y
    def __str__(self):
        return '(' + str(self.__x) + ',' + str(self.__y) + ')'
class CellGrid:
    __rowsize = 0
    __colsize = 0
    __content = None
    __empty = True
    __cellsEmpty = True
    __lastUsedParameters = ('',0,0)
    def __sizerecalc__(self):
        __rows = self.__colsize
        __cols = self.__rowsize
        __diff = __rows * __cols - self.__content.size()
        if __diff > 0:
         self.__content.append([Cell()] * __diff)  # append empty cells at the end
        elif __diff < 0:
         __rows += (-__diff // __cols) + 1  # add enough rows to accommodate all cells
         __extra_cells = __rows * __cols - self.__content.size()
         self.__content.append([Cell()] * __extra_cells)  # expand no. of rows to accept all the extra cells
        self.__colsize = __rows
        self.__rowsize = __cols
    def __init__(self,rows=1,cols=1,cells=None):  # cells is a list of cells, can be empty or a single cell
       self.__rowsize = cols
       self.__colsize = rows
       self.__content = CellArray(cells)
       self.__sizerecalc__()
       self.__empty = False
       self.__cellsEmpty = False
    def get(self):
        return self.__content
    def size(self):
        # l =  self.__content.size()
        # r = l // self.__rowsize - 1
        # if l % self.__rowsize > 0: r += 1
        # self.__rowsize += r
        return xy(self.__rowsize,self.__colsize)
    def get_at(self,XY):
        if isinstance(XY,xy):
            return self.__content.get_at(XY.getx() * self.__rowsize + XY.gety())
        else:
           raise TypeError('Argument should be an XY coordinate pair, but is..' + str(type(XY)))
    def remove_at(self,XY):
        if isinstance(XY,xy):
            if (XY.getx() >= self.__colsize or XY.gety() >= self.__rowsize):
                raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of grid bounds ..' + str(self.size()) )
            index = XY.getx() * self.__rowsize + XY.gety()
            # if index in range(self.size()):
            self.__content.remove_at(index)
            self.__sizerecalc__()
            # else:
            #     raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of bounds 0..' + str(self.size()) )
        else:
           raise TypeError('Argument should be an XY coordinate pair, but is..' + str(type(XY)))
    def insert_at(self,arg,XY):  # insert a cell or a list of cells in a particular position
        if isinstance(XY,xy):
            if (XY.getx() >= self.__colsize or XY.gety() >= self.__rowsize):
                raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of grid bounds ..' + str(self.size()) )
            index = XY.getx() * self.__rowsize + XY.gety()
            if isinstance(arg,list):
                # if index in range(self.__rowsize * self.__colsize):
                    for item in arg:
                     self.__content.insert_at(item,index)
                     index += 1
                    self.__sizerecalc__()
                # else:
                #     raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of grid bounds ..' + str(self.size()) )
            elif isinstance(arg, Cell):
                # if index in range(self.__rowsize * self.__colsize):
                    self.__content.insert_at(arg,index)
                    self.__sizerecalc__()
                # else:
                #     raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of bounds 0..' + str(self.size()) )
            else:
                raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
        else:
           raise TypeError('Argument 2 should be an (x,y) coordinate, but is..' + str(type(XY)))
    def modify_at(self,arg,XY):  # insert a cell or a list of cells in a particular position
        if isinstance(XY,xy):
            if (XY.getx() >= self.__colsize or XY.gety() >= self.__rowsize):
                raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of grid bounds ..' + str(self.size()) )
            index = XY.getx() * self.__rowsize + XY.gety()
            if isinstance(arg,list):
                # if index in range(self.__rowsize * self.__colsize):
                    self.__content.modify_at(arg[0],index)
                    index += 1
                    for item in arg[1:]:
                        self.__content.insert_at(item,index)
                        index += 1
                    self.__sizerecalc__()
                # else:
                #     raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of bounds 0..' + str(self.size()) )
            elif isinstance(arg, Cell):
                # if index in range(self.__rowsize * self.__colsize):
                    self.__content.modify_at(arg,index)
            #     else:
            #         raise IndexError('Index (' + str(XY.getx()) + ',' + str(XY.gety()) + ') out of bounds 0..' + str(self.size()) )
            # # else:
            #     raise TypeError('Argument should be a Cell, but is..' + str(type(arg)))
        else:
           raise TypeError('Argument 2 should be an (x,y) coordinate, but is..' + str(type(XY)))
    def isEmpty(self):
        return self.__empty
    def allCellsEmpty(self):
        self.__empty = False
        for cell in self.__content:
            self.__empty = self.__empty | Cell(cell.isEmpty())
        return self.__empty
    def clear(self):
        self.__content = None
        self.__empty = True
    def clearAll(self):
        for cell in self.__content:
            cell.clear()
        self.__cellsEmpty = True
        self.__empty = False
    def __str__(self):
        return ''.join(str(self.__content))
    def diagonalBandha(self,XY=xy(0,0)):
        self.__lastUsedParameters = ('diagonal Bandha',XY.getx(),XY.gety())
        for (x,y) in zip(range(XY.getx(),self.__rowsize),range(XY.gety(),self.__colsize)):
                yield xy(x,y)
    def rowByrowBandha(self,XY=xy(0,0)):
        self.__lastUsedParameters = ('row by row Bandha',XY.getx(),XY.gety())
        for x in range(XY.getx(),self.__colsize):
            for y in range(XY.gety(),self.__rowsize):
                yield xy(x,y)
    def mukhaBandha(self,XY=xy(0,0)):
        self.__lastUsedParameters = ('mukha Bandha',XY.getx(),XY.gety())
        for y in range(XY.gety(),self.__rowsize):
            for x in range(XY.getx(),self.__colsize):
                yield xy(x,y)
    def lastUsedParameters(self): return self.__lastUsedParameters
