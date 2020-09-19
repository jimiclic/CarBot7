
import tkinter as tk
import random

windowSize = 600 # each pixel will be 2.5 millimeters

car_queue = [] # queue for car rendering

class Car:
    def __init__(self, canvas):
        self.x = 0 # starts at the top left of the arena
        self.y = 0 # may need to change to accommodate for the size of the car
        self.facing = "left" # direction car is facing
        self.draw(canvas)

    def draw(self, canvas):
        if len(car_queue) != 0:
            canvas.delete(car_queue[0])
            car_queue.pop()

        carLength = 100 # length of car in millimeters rounded up
        carWidth = 80 # width of car in millimeters rounded up
        
        if self.facing == "left" or self.facing == "right": # drawing the rectangle based on which direction the car is facing
            carShape = canvas.create_rectangle(self.x - carLength, self.y - carWidth, \
                self.x + carLength, self.y + carWidth, fill = 'blue')
        else:
            carShape = canvas.create_rectangle(self.x - carLength, self.y - carWidth, \
                self.x + carLength, self.y + carWidth, fill = 'blue')
        car_queue.append(carShape)
# gonna need to see what arduino is going to input in order to move car on grid

def main():
    window = tk.Tk() # setting up the window
    canvas = tk.Canvas(window, width = windowSize, height = windowSize, bg = 'black')
    canvas.pack()

    for x in range(0, 600, 20): # creating a grid with squares of 50 mm^2 or 5 cm^2
        canvas.create_line(x, 0, x, 600, fill = 'white')
    for y in range(0, 600, 20):
        canvas.create_line(0, y, 600, y, fill = 'white')

    car = Car(canvas)

    window.mainloop()
main()