import tkinter as tk

import serial
import time
import sys
import signal


# pixel to cm ratio
global pixCmRatio
pixCmRatio = 5 # every 5 pixels represents 1 cm
# global emptyAreaWidth
#emptyAreaWidth = 25 # empty space (in cm) on the edge left for the car to pass

# list of objects detected
objs = []
# new measurements queue
newMeasure = []
# turn number
global turnNum
turnNum = 0

##############################################################################

# functions

# edit the detected object corner coordinates based on the coordinate (in cm)
def editObj(x, y):
    # find match
    for i in range(len(objs)):
        obj = objs[i]
        if len(obj.coordinates) != 3 or i == 0:
            for i in range(len(obj.coordinates)):
                coord = obj.coordinates[i]
                # if x and y match (with 2 cm of possible error)
                xMatch = abs(x - coord[0]) <= 2
                yMatch = abs(y - coord[1]) <= 2
                # coordinate already existed
                if xMatch and yMatch or \
                len(obj.coordinates) == 2 and abs(x - obj.coordinates[1][0]) <= 2 and abs(y - obj.coordinates[1][1]) <= 2: 
                    return
                # new coordinate for detected object
                elif xMatch:
                    # check if distance is not too large (the largest box length is 14 [plus 2 cm error]
                    if abs(y - coord[1]) > 16:
                        break
                    else:
                        obj.coordinates.append([coord[0], y])
                        return
                elif yMatch:
                    # check if distance is not too large (the largest box length is 14 [plus 2 cm error]
                    if abs(x - coord[0]) > 16:
                        break
                    else:
                        obj.coordinates.append([x, coord[1]])
                        return
    obj = RectangleObj(x, y)
    objs.append(obj)

##############################################################################

# bluetooth
class Bluetooth:
    # set up com port and baudrate
    def __init__(self):
        self.COM = input("Enter the COM Port: \n")
        self.BAUD = input("Enter the Baudrate: \n")
        self.SerialPort = serial.Serial(self.COM,self.BAUD,timeout=1)

    # read data
    def readData(self):
        raw = self.SerialPort.readline().decode('utf-8')
        if (raw):
            # turn signal
            if raw == "-1":
                turn += 1
            # mapping ended signal
            elif raw == "-2":
                return false
            # new measurements
            else:
                data = raw.split(",")
                for d in data:
                    d = int(d)
                # format [front, left, right]
                newMeasure.append(data)
        return true

    def debugging(self):
        incoming = self.SerialPort.readline()
        if (incoming):
            print((incoming).decode('utf-8'))
        
##############################################################################

# object
class RectangleObj:
    def __init__(self, x, y):
        self.coordinates = [[x, y]]

    # draw object
    def draw(self, canvas):
        # corner 1 and corner 2 index
        c1 = 0
        c2 = 2 
        # in case that the line formed by corner 1 and corner 2 is not the diagnal line, switch c1
        if self.coordinates[c1][0] == self.coordinates[c2][0] or self.coordinates[c1][1] == self.coordinates[c2][1]:
            c1 = 1
        # draw rectangle
        canvas.create_rectangle((self.coordinates[c1][0]) * pixCmRatio,
                                    (self.coordinates[c1][1]) * pixCmRatio,
                                    (self.coordinates[c2][0]) * pixCmRatio,
                                    (self.coordinates[c2][1]) * pixCmRatio,
                                    fill='red')


        """
    # draw object
    def drawv2(self, canvas):
        # corner 1 and corner 2 index
        c1 = 0
        c2 = 2
        # rare case which only 2 corners are mapped
        if len(self.coordinates) == 2:
            # equal x coordinate
            if self.coordinates[0][0] == self.coordinates[1][0]:   
                canvas.create_rectangle((self.coordinates[0][0]) * pixCmRatio,
                                    (self.coordinates[0][1]) * pixCmRatio,
                                    (self.coordinates[1][0]) * pixCmRatio,
                                    (self.coordinates[1][1]) * pixCmRatio,
                                    fill='red')
            # equal y coordinate
            else:
                canvas.create_rectangle((self.coordinates[0][0]) * pixCmRatio,
                                    (self.coordinates[0][1]) * pixCmRatio,
                                    (self.coordinates[1][0]) * pixCmRatio,
                                    (self.coordinates[1][1] + 10) * pixCmRatio,
                                    fill='red')
        
        else: 
            # in case that the line formed by corner 1 and corner 2 is not the diagnal line, switch c1
            if self.coordinates[c1][0] == self.coordinates[c2][0] or self.coordinates[c1][1] == self.coordinates[c2][1]:
                c1 = 1
            # draw rectangle
            canvas.create_rectangle((self.coordinates[c1][0]) * pixCmRatio,
                                    (self.coordinates[c1][1]) * pixCmRatio,
                                    (self.coordinates[c2][0]) * pixCmRatio,
                                    (self.coordinates[c2][1]) * pixCmRatio,
                                    fill='red')
        """

    # for debugging
    def printObj(self):
        print(self.coordinates)
    
##############################################################################
        
# car
class Car:
    def __init__(self):
        # length and width (rounded)
        self.LEN = 24
        self.WID = 18

    # process measurement
    def measurementProcess(self):
        while(len(newMeasure) > 0):
            # calculate x and y coordinate in cm
            if turnNum == 0:
                x = 150 - newMeasure[0][0] - self.LEN / 2
                y = newMeasure[0][1] + newMeasure[0][2] + self.WID
            elif turnNum == 1:
                x = 150 - newMeasure[0][1] - newMeasure[0][2] - self.WID
                y = 150 - newMeasure[0][0] - self.LEN / 2
            elif turnNum == 2:
                x = newMeasure[0][0] + self.LEN / 2
                y = 150 - newMeasure[0][1] - newMeasure[0][2] - self.WID
            else:
                x = newMeasure[0][1] + newMeasure[0][2] + self.WID
                y = newMeasure[0][0] + self.LEN / 2
            editObj(x, y)
            newMeasure.pop(0)
                
##############################################################################

# main function
def main():
    # keep looping
    loop = true
    # set up bluetooth
    bt = Bluetooth()
    # set up car
    car = Car()

    print("Mapping...")

    # mapping loop
    while loop:
        # get bluetooth input
        loop = bt.readData()
        # process data
        car.measurementProcess
    
    # mapping finished -> set up window
    window = tk.Tk()
    canvas = tk.Canvas(window, width=150*pixCmRatio, height=150*pixCmRatio, bg='black') 
    canvas.pack()

    # draw all objects
    for obj in objs:
        obj.draw(canvas)

    window.mainloop()

                                           
# test
def test():
    editObj(1, 1)
    editObj(10, 2)
    editObj(18, 1)
    editObj(30, 1)
    editObj(30, 1)
    editObj(30, 9)
    editObj(30, 40)
    editObj(30, 50)
    editObj(30, 50)
    editObj(30, 50)
    editObj(18, 50)
    editObj(10, 50)
    editObj(2, 50)
    editObj(2, 50)
    editObj(2, 40)
    editObj(2, 9)
    editObj(2, 1)

    for obj in objs:
        obj.printObj()

    # mapping finished -> set up window
    window = tk.Tk()
    canvas = tk.Canvas(window, width=150*pixCmRatio, height=150*pixCmRatio, bg='black') 
    canvas.pack()

    # draw all objects
    for obj in objs:
        obj.draw(canvas)

    window.mainloop()

# bluetooth test
def testB():
    bt = Bluetooth()

    while 1:
        bt.debugging()
        
    
if __name__ == "__main__":
    test()
