import tkinter as tk

import serial
import time
import sys
import signal


# grid and pixel to cm ratio
global gridSize
global pixCmRatio
global emptyAreaWidth
gridSize = 5 # each grid is 5 cm wide
pixCmRatio = 5 # every 5 pixels represents 1 cm
emptyAreaWidth = 25 # empty space (in cm) on the edge left for the car to pass

# list of objects detected
objs = []

##############################################################################

# functions

# edit the object coordinates based on new grid coordinate
def editObj(x, y):
    index = 0
    # find match
    for obj in objs:
        for coord in obj.coordinates:
            # if x and y match (with 1 grid possible error)
            xMatch = abs(x - coord[0]) <= 1
            yMatch = abs(y - coord[1]) <= 1
            # coordinate already existed
            if xMatch and yMatch:
                return 
            # new coordinate for detected object
            else if xMatch:
                obj.coordinates.append([coord[0], y])
                return
            else if yMatch:
                obj.coordinates.append([x, coord[1])
                return
        index += 1
    # not found (new object detected)
    obj = RectangleObj(x, y)
    objs.append(obj)

##############################################################################

# bluetooth


##############################################################################

# object
class RectangleObj:
    def __init__(self, x, y):
        self.coordinates = [[x, y]]

    # add coordinate
    def addCoordinate(self, x, y):
        self.coordinates.append([x,y])

    # draw object
    def draw(self, canvas):
        canvas.create_rectangle((self.coordinates[0][0] * gridSize + emptyAreaWidth) * pixCmRatio,
                                (self.coordinates[0][1] * gridSize + emptyAreaWidth) * pixCmRatio,
                                (self.coordinates[2][0] * gridSize + emptyAreaWidth) * pixCmRatio,
                                (self.coordinates[2][1] * gridSize + emptyAreaWidth) * pixCmRatio,
                                fill='red')
    
##############################################################################

# car
class Car:
    def __init__(self):
        # length and width
        self.wid = 24.2
        self.len = 17.4
        # position (in grid coordinate)
        self.x = 0
        self.y = 0

    # move the car to given position
    def move(self):
        pass

    # turn the car 90 degrees
    def turn(self):
        pass

    # measure the distance
    def measure(self, axis, turnCount, previous):
        # get measurement (need fix)
        distance = 0 # distance in cm
        # if measurement is not around (150 - car width/lengh?) cm or not the same as the previous measurement (error: 5 cm)
        if abs(150 - (distance + self.wid)) >= 5 and abs(previous - distance) >= 5
            # convert distance to grid number
            gridNum = (distance - (emptyAreaWidth - self.wid) // gridSize) + 1
            # process measurement
            measurementProcess(self, gridNum, axis, turnCount)
        # return current measurement (pass to previous measurement)
        return distance

    # process measurement
    def measurementProcess(self, gridNum, axis, turnCount):
        if axis == 'x':
            # search for coordinate
            search = searchObj(self.x, gridNum)
        else:
            # search for coordinate
            search = searchObj(gridNum, self.y)
        # coordinate not found
        if search == -2:
            #create new object
        # new coordinate for existing object
        else if search >= 0:
            
                

    # detect the edge of the arena (I'm not sure if it is necessary)
    def detectEdge(self):
        pass 

##############################################################################

# main function
def main():
    # set up window
    window = tk.Tk()
    canvas = tk.Canvas(window, width=150*pixCmRatio, height=150*pixCmRatio, bg='black') 
    canvas.pack()

    # need current object and previous measurement

    print(gridSize, pixCmRatio)

    window.mainloop()

# test
def test():
    pass
    
if __name__ == "__main__":
    main()
