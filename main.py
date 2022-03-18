import random
import numpy as np
import matplotlib.pyplot as plt


class Neighbourhood:
    pooltotalEnergyCost = 0
    pooltotalEnergyUse = 0
    poolEnergyCostHourly = [0]*24
    poolEnergyUseHourly = [0] * 24

    def __init__(self, households):
        self.households = households
        for house in households:
            self.poolEnergyCostHourly = [ self.poolEnergyCostHourly[x] + house.energyCostHourly[x] for x in range (len (self.poolEnergyCostHourly))]
            self.poolEnergyUseHourly = [ self.poolEnergyUseHourly[x] + house.energyUseHourly[x] for x in range (len (self.poolEnergyUseHourly))]
        for hourlyCost in self.poolEnergyCostHourly:
            self.pooltotalEnergyCost += hourlyCost
        for hourlyUse in self.poolEnergyUseHourly:
            self.pooltotalEnergyUse += hourlyUse


class Household:
    totalEnergyCost = 0
    energyCostHourly = [0]*24
    energyUseHourly = [0] * 24
    timeslots = []
    houseHasEV = True
    hasShiftApp = [True, False, True, False, True]
    hasNonShiftApp = [True, False, True]

    def __init__(self, viableTimeslots):
        # on init, run random assignment of appliences
        #0-10 shiftableAppiances, scheduledAppliances
        shift_appliances = [boolroll(40)] + [True for x in range(len(shiftableAppiances)-1)]
        scheduled_appliances = [True for x in range(len(scheduledAppliances))]
        extra_appliances = [boolroll(60) for x in range(len(extraAppliances))]


        # fill shiftable timeslot
        for index, hasItem in enumerate(shift_appliances):
            if hasItem == True:
                # add ot
                rand_index = random.randint(0, len(viableTimeslots)-1)
                chosenTimeslot = viableTimeslots[rand_index]
                price_of_use = daysPrice.prices[chosenTimeslot] * (shiftAppPower[index]/1000)
                self.energyCostHourly[chosenTimeslot] += price_of_use
                self.energyUseHourly[chosenTimeslot] += shiftAppPower[index]

        #fill base timeslots
        for index, hasItem in enumerate(scheduled_appliances):
            if hasItem == True:
                rand_index = random.randint(0, 23)
                price_of_use = daysPrice.prices[rand_index] * (schedAppPower[index] / 1000)
                self.energyCostHourly[rand_index] += price_of_use
                self.energyUseHourly[rand_index] += schedAppPower[index]

        #fill random items timeslots
        for index, hasItem in enumerate( extra_appliances):
            if hasItem == True:
                rand_index = random.randint(0, 23)
                price_of_use = daysPrice.prices[rand_index] * (extraAppPower[index] / 1000)
                self.energyCostHourly[rand_index] += price_of_use
                self.energyUseHourly[rand_index] += extraAppPower[index]



class DailyPricing:
    def __init__(self, dayMin, dayMax):
        self.dayMax = dayMax
        self.dayMin = dayMin
        self.timeTeller = 24
        self.prices = [0] * self.timeTeller
        for index in range(self.timeTeller):
            self.prices[index] = random.randint(self.dayMin, self.dayMax - 5)
        peakhour = random.randint(8, 20)
        self.prices[peakhour:peakhour + 3] = [random.randint(self.dayMax - 20, self.dayMax),
                                              random.randint(self.dayMax - 20, self.dayMax),
                                              random.randint(self.dayMax - 20, self.dayMax)]


def findGoodTimeslots(myprices):
    # three strategies = disregard energy cost, avoid tops, seek out bottoms
    high_percentile = np.percentile(myprices, 80)
    low_precentile = np.percentile(myprices, 20)
    print("avoid tops: ", high_percentile, "seek bottoms: ", low_precentile)

    avg = sum(myprices) / len(myprices)
    print("The average spotpris is ", round(avg, 2), " øre/kWt")
    timeslots = []
    for index, price in enumerate(myprices):
        #change price comparison for different strategies.
        if price < low_precentile:
            timeslots.append(index)
    return timeslots


def boolroll(chance):
    baseline = random.randint(0, 100)
    if chance > baseline:
        return True
    else:
        return False


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


shiftableAppiances = ["Electric Vehicle", "Dishwasher", "Laundry Machine", "Cloth Dryer", ]
shiftAppPower = [9900, 1440, 1940, 2500]
scheduledAppliances = ["Ligtning", "Heating", "Refridgeration", "Electric stove", "TV", "Computer"]
schedAppPower = [200, 6000, 3000, 3900, 300, 600]
extraAppliances = ["coffee maker", "ceiling fan", "hair dryer", "toaster", "microwave",
                   "router", "cellphone charger", "cloth iron", "separate freezer"]
extraAppPower = [100, 100, 100, 1000, 1000, 1000, 1000, 100, 1000]


print_hi('PyCharm')
daysPrice = DailyPricing(20, 80)
print(daysPrice.prices)


bestTimeslots = findGoodTimeslots(daysPrice.prices)
print(bestTimeslots)


houses = [Household(bestTimeslots) for x in range(30)]
myNeighbourhood = Neighbourhood(houses)

print(myNeighbourhood.poolEnergyUseHourly)
print(myNeighbourhood.poolEnergyCostHourly)
print("avg home uses ", myNeighbourhood.pooltotalEnergyCost/30/100, "kr")

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Neighbourhood energy use vs cost of energy in øre/kwh')
ax1.plot(list(range(0, 24)), [x/(1000) for x in myNeighbourhood.poolEnergyUseHourly], label="Energy usage")
ax2.plot(list(range(0, 24)), daysPrice.prices, label="cost øre/KWT")

plt.show()

