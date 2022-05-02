import math
import random

class Player:

    x = 0
    y = 0
    homex = 0
    homey = 0
    modifier = 0.0
    sigma = 1
    Z = 1500
    dist2home = 0.0
    neighborDist = 0.0
    neighborHouseDist = 0.0
    storeDist = 0.0

    def __init__(self,x,y,homex,homey,mod):
        self.x = x
        self.y = y
        self.homex = homex
        self.homey = homey
        self.modifier = mod
        deltax = abs(self.x - self.homex)
        deltay = abs(self.y - self.homey)
        self.dist2home = math.sqrt((deltax ** 2) + (deltay ** 2))

    def location(self):
        return self.x, self.y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def gethomex(self):
        return self.homex

    def gethomey(self):
        return self.homey

    def setNeighborHouseDist(self,neighborHouseDist):
        self.neighborHouseDist = neighborHouseDist

    def getNeighborHouseDist(self):
        return self.neighborHouseDist

    def move(self, destx, desty):
        self.x = destx
        self.y = desty
        deltax = abs(self.x - self.homex)
        deltay = abs(self.y - self.homey)
        self.dist2home = math.sqrt((deltax ** 2) + (deltay ** 2))

    def __str__(self):
        ans = "Current Location: " + str(self.x) + "," + str(self.y) + "\t"
        ans = ans + "Home Location: " + str(self.homex) + "," + str(self.homey)
        return ans

    def distanceto(self,other):
        (otherx,othery) = other.location()
        deltax = abs(self.x-otherx)
        deltay = abs(self.y-othery)
        return math.sqrt((deltax**2)+(deltay**2))

    def distancetohome(self,other):
        otherx = other.gethomex()
        othery = other.gethomey()
        deltax = abs(self.x-otherx)
        deltay = abs(self.y-othery)
        return math.sqrt((deltax**2)+(deltay**2))

    def setNeighborDist(self,neighborDist):
        self.neighborDist = neighborDist

    def getNeighborDist(self):
        return self.neighborDist

    def setStoreX(self,storeX):
        self.storex = storeX

    def getStoreX(self):
        return self.storex

    def setStoreY(self,storeY):
        self.storey = storeY

    def getStoreY(self):
        return self.storey

    def setStoreDist(self, storeDist):
        self.storeDist = storeDist

    def getStoreDist(self):
        return self.storeDist

    def getdistancetohome(self):
        return self.dist2home

    def incentivize(self, alpha, beta):
        self.alpha = alpha * self.modifier
        self.beta = beta * self.modifier
        self.sigma = (1 - self.modifier)

    def movetowards(self, destx, desty):
        if(destx > self.x):
            self.x = self.x + 1
        elif(destx < self.x):
            self.x = self.x - 1
        else:
            self.x = self.x
        if(desty > self.y):
            self.y = self.y + 1
        elif(desty < self.y):
            self.y = self.y - 1
        else:
            self.y = self.y
        deltax = abs(self.x - self.homex)
        deltay = abs(self.y - self.homey)
        self.dist2home = math.sqrt((deltax ** 2) + (deltay ** 2))

    def gohome(self):
        if (self.homex > self.x):
            self.x = self.x + 1
        elif (self.homex < self.x):
            self.x = self.x - 1
        else:
            self.x = self.x
        if (self.homey > self.y):
            self.y = self.y + 1
        elif (self.homey < self.y):
            self.y = self.y - 1
        else:
            self.y = self.y
        deltax = abs(self.x - self.homex)
        deltay = abs(self.y - self.homey)
        self.dist2home = math.sqrt((deltax ** 2) + (deltay ** 2))

    def goout(self):
        if (self.storex > self.x):
            self.x = self.x + 1
        elif (self.storex < self.x):
            self.x = self.x - 1
        else:
            self.x = self.x
        if (self.storey > self.y):
            self.y = self.y + 1
        elif (self.storey < self.y):
            self.y = self.y - 1
        else:
            self.y = self.y
        deltax = abs(self.x - self.homex)
        deltay = abs(self.y - self.homey)
        self.dist2home = math.sqrt((deltax ** 2) + (deltay ** 2))

    def decide(self):
        home = self.alpha*math.log10(self.Z) + self.beta*math.log10(self.neighborHouseDist+1)
        mobile1 = self.alpha*math.log10(self.Z - (self.dist2home+1))
        mobile2 = self.beta*(self.neighborDist+1)
        mobile3 = self.sigma*(1/(self.storeDist+1))
        mobile = mobile1 + mobile2 + mobile3
        if (home > mobile):
            return 0
        elif(mobile > home):
            return 1
        else:
            return random.randint(0,1)
