import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns

class Store:

    x = 0
    y = 0


    def __init__(self,x,y):
        self.x = x
        self.y = y

    def location(self):
        return self.x, self.y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def __str__(self):
        return ("Store Location: " + str(self.x) + "," + str(self.y))

    def distanceto(self,other):
        (otherx,othery) = other.location()
        deltax = abs(self.x-otherx)
        deltay = abs(self.y-othery)
        return math.sqrt((deltax**2)+(deltay**2))
