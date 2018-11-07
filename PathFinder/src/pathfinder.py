'''
Created on Nov 5, 2018

@author: Rebecca
'''

from functools import wraps
from time import time

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print ('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap

class PathFinder:
    DEST=2
    EMPTY=0
    SOURCE=99
    PATH=98
    
    def __init__(self, aMap):
        self.width = 5
        self.height = 5
        self.currentRow = 0
        self.currentCol = 0
        self.currentWave = PathFinder.DEST
        self.map = aMap

    def printMap(self):
        for row in range(self.width):
            mapRow = ''
            for col in range(self.height):
                if self.map[row][col] == 99:
                    mapRow += '  S'
                elif self.map[row][col] == 98:
                    mapRow += '  *'
                elif self.map[row][col] == 2:
                    mapRow += '  G'
                elif self.map[row][col] == 1:
                    mapRow += '  X'
                elif self.map[row][col] == 0:
                    mapRow += '  O'
                else:
                    mapRow += '{0: 3d}'.format(self.map[row][col])
            print(mapRow)
    
    def setLocation(self, coords):
        self.currentRow = coords[0]
        self.currentCol = coords[1]
        
    def getCurrentWaveLocations(self):
        ''' returns list of coordinates of all specified wave locations '''
        locations = []
        for row in range(self.width):
            for col in range(self.height): 
                if self.map[row][col] == self.currentWave:
                    locations.append([row, col])
        return locations
    
    def getLocation(self, target):   
        ''' returns coordinates of specified locations '''
        for row in range(self.width):
            for col in range(self.height): 
                if self.map[row][col] == target:
                    return([row, col])
        return []
    
    def setNextWave(self):
        # update north
        if self.currentRow > 0:
            if self.map[self.currentRow - 1][self.currentCol] == 0:
                self.map[self.currentRow - 1][self.currentCol] = self.currentWave + 1
        # update west
        if self.currentCol > 0:
            if self.map[self.currentRow][self.currentCol - 1] == 0:
                self.map[self.currentRow][self.currentCol - 1] = self.currentWave + 1
        # update east
        if self.currentCol < self.width-1:
            if self.map[self.currentRow][self.currentCol + 1] == 0:
                self.map[self.currentRow][self.currentCol + 1] = self.currentWave + 1
        # update south
        if self.currentRow < self.height-1:
            if self.map[self.currentRow + 1][self.currentCol] == 0:
                self.map[self.currentRow + 1][self.currentCol] = self.currentWave + 1
    
    def emptyElementsExist(self):
        for row in range(self.width):
            for col in range(self.height): 
                if self.map[row][col] == PathFinder.EMPTY:
                    return True
    
    @timing            
    def wavefront(self):
        ''' intuitive implementation that follows pseudocode description. Also
            fastest runtime. '''
        while self.emptyElementsExist():
            print('Wave {}'.format(self.currentWave))
            for currentWaveLocation in self.getCurrentWaveLocations():
                self.setLocation(currentWaveLocation)
                self.setNextWave()
            self.currentWave += 1
            self.printMap()
    
    @timing
    def buildwf(self):
        ''' PLTW solution in C/C++ style - not sure why they eschewed for loops 
            and their own pseudocode...'''
        progress=0
        numloops=self.width*self.height
        while progress<numloops:
            self.currentRow=0
            print('Wave: {}'.format(self.currentWave))
            while self.currentRow<self.height:
                self.currentCol=0
                while self.currentCol<self.width:
                    if self.map[self.currentRow][self.currentCol] == self.currentWave:
                        # update north
                        if self.currentRow > 0:
                            if self.map[self.currentRow - 1][self.currentCol] == 0:
                                self.map[self.currentRow - 1][self.currentCol] = self.currentWave + 1
                        # update west
                        if self.currentCol > 0:
                            if self.map[self.currentRow][self.currentCol - 1] == 0:
                                self.map[self.currentRow][self.currentCol - 1] = self.currentWave + 1
                        # update east
                        if self.currentCol < self.width-1:
                            if self.map[self.currentRow][self.currentCol + 1] == 0:
                                self.map[self.currentRow][self.currentCol + 1] = self.currentWave + 1
                        # update south
                        if self.currentRow < self.height-1:
                            if self.map[self.currentRow + 1][self.currentCol] == 0:
                                self.map[self.currentRow + 1][self.currentCol] = self.currentWave + 1
                    self.currentCol += 1
                self.currentRow += 1
            progress += 1
            self.currentWave += 1
            self.printMap()
    
    @timing
    def buildwf2(self):
        ''' PLTW version but with end condition checking and for loops - still
            slower than my version with extra loops and method calls...'''
        while self.emptyElementsExist():
            print('Wave: {}'.format(self.currentWave))
            
            for row in range(self.height):
                for col in range(self.width):
                    if self.map[row][col] == self.currentWave:
                        self.currentRow=row
                        self.currentCol=col
                        self.setNextWave()
            self.currentWave += 1
            self.printMap()
                       
    def arrived(self):
        if self.getLocation(PathFinder.DEST) == [self.currentRow, self.currentCol]:
            return True
        return False
                
    def moveTowardsDestination(self):
        pathValues = [101, 101, 101, 101]
        
        # Show current location as part of the path
        self.map[self.currentRow][self.currentCol] = PathFinder.PATH
        
        # add north
        if self.currentRow > 0:
            pathValues[0] = self.map[self.currentRow - 1][self.currentCol]    
        # add west
        if self.currentCol > 0:
            pathValues[1] = self.map[self.currentRow][self.currentCol - 1]
        # add east
        if self.currentCol < self.width-1:
            pathValues[2] = self.map[self.currentRow][self.currentCol + 1]
        # add south
        if self.currentRow < self.height-1:
            pathValues[3] = self.map[self.currentRow + 1][self.currentCol]
        
        # translate any 1's to a really high value so it is not chosen
        pathValues = [101 if n == 1 else n for n in pathValues]  
        low_index = pathValues.index(min(pathValues))
        if low_index == 0:
            # go north
            self.currentRow = self.currentRow - 1
        elif low_index == 1:
            # go west
            self.currentCol = self.currentCol - 1
        elif low_index == 2:
            # go east
            self.currentCol = self.currentCol + 1
        elif low_index == 3:
            # go south 
            self.currentRow = self.currentRow + 1
        
        if self.arrived():
            return True
        else:    
            # Set source target marker to new location
            self.map[self.currentRow][self.currentCol] = PathFinder.SOURCE
            return False
    
    @timing           
    def pathfinder(self):
        self.setLocation(self.getLocation(PathFinder.SOURCE))
        print('Start Location: {},{}'.format(self.currentRow, self.currentCol))
        while not self.moveTowardsDestination():
            print('New Location: {},{}'.format(self.currentRow, self.currentCol))
            self.printMap()
        print('Path complete!')
            
if __name__ == '__main__':
    aMap = [[0, 0, 0, 0, 0],
           [0, 1, 99, 1, 0],
           [1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 2, 0, 0]]

    p = PathFinder(aMap)
    
    p.wavefront()
    print('Finished wavefront - calling buildwf...')
    aMap = [[0, 0, 0, 0, 0],
           [0, 1, 99, 1, 0],
           [1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 2, 0, 0]]
    p = PathFinder(aMap)
    p.buildwf()
    print('Finished buildwf - calling buildwf2...')
    aMap = [[0, 0, 0, 0, 0],
           [0, 1, 99, 1, 0],
           [1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 2, 0, 0]]
    p = PathFinder(aMap)
    p.buildwf2()
    
    p.pathfinder()
    
    aMap = [[0, 0, 0, 0, 1],
           [0, 1, 0, 0, 0],
           [99, 1, 1, 1, 0],
           [0, 0, 0, 1, 2],
           [0, 1, 0, 0, 0]]

    p = PathFinder(aMap)
    p.wavefront()
    print('Finished wavefront - calling buildwf...')
    aMap = [[0, 0, 0, 0, 1],
           [0, 1, 0, 0, 0],
           [99, 1, 1, 1, 0],
           [0, 0, 0, 1, 2],
           [0, 1, 0, 0, 0]]
    p = PathFinder(aMap)
    p.buildwf()
    
    print('Finished buildwf - calling buildwf2...')
    aMap = [[0, 0, 0, 0, 1],
           [0, 1, 0, 0, 0],
           [99, 1, 1, 1, 0],
           [0, 0, 0, 1, 2],
           [0, 1, 0, 0, 0]]
    p = PathFinder(aMap)
    p.buildwf2()
    
    
    p.pathfinder()
    
    
    