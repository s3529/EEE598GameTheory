import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import imageio

from player import Player
from store import Store

filenames = []

# Updates each player to determine their distance from their closet neighbor not in their house
def updateNeighbors():
    for i in range(populationN):
        closest = 150 # larger than the max distance on a 100 by 100 grid
        for j in range(populationN):
            if (i != j):
                if(((population[j].getx()==population[j].gethomex())&(population[j].getx()==population[j].gethomex()))):
                    closest = closest
                else:
                    if (population[i].distanceto(population[j]) <= closest):
                        closest = population[i].distanceto(population[j])
                    else:
                        closest = closest
            else:
                closest = closest
        if closest == 150:
            closest = 0
        population[i].setNeighborDist(closest)

# Updates each player to determine their home's distance from the nearest home
def updateHousing():
    for i in range(populationN):
        closest = 150 # larger than the max distance on a 100 by 100 grid
        for j in range(populationN):
            if (i != j):
                distance = math.sqrt((population[i].gethomex()-population[j].gethomex())**2 + (population[i].gethomey()-population[j].gethomey())**2)
                if (distance <= closest):
                    closest = population[i].distancetohome(population[j])
                else:
                    closest = closest
            else:
                closest = closest
        population[i].setNeighborHouseDist(closest)

# Updates each player to determine their distance from their closest store
def updateStores():
    for i in range(populationN):
        closest = 150
        preferred = 0
        for j in range(storesN):
            if (population[i].distanceto(stores[j]) <= closest):
                closest = population[i].distanceto(stores[j])
                preferred = j
            else:
                closest = closest
        else:
            closest = closest
        population[i].setStoreX(stores[preferred].getx())
        population[i].setStoreY(stores[preferred].gety())
        population[i].setStoreDist(closest)

# Generates a graphical map of where each player, home and store is
def mapplot(t):
    playerXvals = np.zeros(populationN)
    playerYvals = np.zeros(populationN)
    for i in range(populationN):
        playerXvals[i] = population[i].getx()
        playerYvals[i] = population[i].gety()

    homeXvals = np.zeros(populationN)
    homeYvals = np.zeros(populationN)
    for i in range(populationN):
        homeXvals[i] = population[i].gethomex()
        homeYvals[i] = population[i].gethomey()

    storeXvals = np.zeros(storesN)
    storeYvals = np.zeros(storesN)
    for i in range(storesN):
        storeXvals[i] = stores[i].getx()
        storeYvals[i] = stores[i].gety()

    plt.plot(playerXvals, playerYvals, 'o', label = 'Players')
    plt.plot(homeXvals, homeYvals, 's', label = 'Homes', alpha=0.5)
    plt.plot(storeXvals, storeYvals, '*', label = 'Shops', alpha=0.5)
    plt.legend(bbox_to_anchor =(0.75, 1.15), ncol = 3)
    title = "Improved Solution Turn " + str(t)
    plt.title(title)
    filename = f'{t}.png'
    filenames.append(filename)
    plt.savefig(filename)
    plt.close()

# City size
cityX = 1000
cityY = 1000

# Number of stores
storesN = 50
stores = []

# Population size
populationN = 100
population = []

# Incentives given
alpha = 3
beta = 1

turns = 350
history = np.zeros((populationN,turns))

# Randomly generates a population with each having a home location and incentive modifier
for i in range(populationN):
    homex = random.randint(0, cityX)
    homey = random.randint(0, cityY)

    # Improved simulation with modifier
    if i < populationN * .7:
        mod = 1 # assuming 70% of population fully values incentives
    elif (i < populationN * .9) & (i >= populationN * .7):
        mod = 0.5 # assuming 20% of population discounts incentives by 50%
    else:
        mod = 0.2 # assuming 10% of population discounts incentives by 80%

    # Original simulation without modifier
    # mod = 1
    playeri = Player(homex, homey, homex, homey, mod)
    population.append(playeri)

# Randomly generates a city with a certain number of stores
for i in range(storesN):
    x = random.randint(0, cityX)
    y = random.randint(0, cityY)
    storei = Store(x, y)
    stores.append(storei)

# tells each player how much the incentives
for i in range(populationN):
    population[i].incentivize(alpha,beta)

mapplot(0)
updateNeighbors()
updateStores()
updateHousing()

for t in range(turns):
    print("TURN ",t)
    for i in range(populationN):
        choice = population[i].decide()
        history[i,t] = choice
        if choice == 0:
            population[i].gohome()
            result = "to go home"
        else:
            population[i].goout()
            result = "to go out"
        print("\tI am player", i, "and I choose", result)
    updateNeighbors()
    updateStores()
    updateHousing()
    mapplot(t)

with imageio.get_writer('mygif.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.v2.imread(filename)
        writer.append_data(image)

for filename in set(filenames):
    os.remove(filename)

average = np.zeros(populationN)
for i in range(populationN):
    total = 0
    avg = 0
    for t in range(turns):
        total = total + history[i,t]
    avg = total/turns
    average[i] = avg

plt.plot(range(populationN), average, 'x')
plt.title("% of time spent Going Out")
plt.show()