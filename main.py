import random
import numpy as np

class Neighbourhood:
    households = []

    def __init__(self, name, age):
        self.name = name
        self.age = age

class Households:
    houseHasEV = True
    hasShiftApp = [True, False, True, False, True]
    hasNonShiftApp = [True, False, True]

    def __init__(self, name, age):
        self.name = name
        self.age = age

class DailyPricing:
    def __init__(self, dayMin, dayMax):
        self.dayMax = dayMax
        self.dayMin = dayMin
        self.timeTeller = 24
        self.prices = [0]*self.timeTeller
        for index in range(self.timeTeller):
            #random.randint(self.dayMin, self.dayMax)
            y = np.sin(index/3.14+3.14) + np.random.normal(scale=0.4)
            diff = dayMax-dayMin
            self.prices[index] = y*(diff/2)+dayMax


def findGoodTimeslots(myprices):
    #find avg prrice, return array of good timeslots
    avg = sum(myprices) / len(myprices)
    print("The average is ", round(avg, 2))
    timeslots = []
    for index, price in enumerate(myprices):
        if price < avg:
            timeslots.append(index)
    return timeslots

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

shiftableAppiances = ["Dishwasher", "Laundry Machine", "Cloth Dryer", "Electric Vehicle"]
shiftAppPower = [1440, 1940, 2500, 9900]
scheduledAppliances = ["Ligtning", "Heating", "Refridgeration", "Electric stove", "TV", "Computer"]
schedAppPower = [2000, 8000, 3000, 3900, 300, 600]
extraAppliances = ["coffee maker", "ceiling fan", "hair dryer", "toaster", "microwave",
                      "router","cellphone charger", "cloth iron", "separate freezer"]
extraAppPower = [100, 100, 100, 1000, 1000, 1000, 1000, 100, 1000]

if __name__ == '__main__':
    print_hi('PyCharm')
    daysPrice = DailyPricing(20, 80)
    print(daysPrice.prices)
    print(findGoodTimeslots(daysPrice.prices))






