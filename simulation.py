import numpy as np

class individual:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y

    def move(self, move_x, move_y):
        self.x += move_x
        self.y += move_y

    def location(self):
        print("current location is in x: {} y: {}".format(self.x, self.y))