import random
import numpy as np
import matplotlib.pyplot as plt

class Neighbourhood:
    pooltotalEnergyCost = 0
    pooltotalEnergyUse = 0
    poolEnergyCostHourly = [0] * 24
    poolEnergyUseHourly = [0] * 24

    def __init__(self, households):
        self.households = households
        for house in households:
            self.poolEnergyCostHourly = [self.poolEnergyCostHourly[x] + house.energyCostHourly[x] for x in
                                         range(len(self.poolEnergyCostHourly))]
            self.poolEnergyUseHourly = [self.poolEnergyUseHourly[x] + house.energyUseHourly[x] for x in
                                        range(len(self.poolEnergyUseHourly))]
        for hourlyCost in self.poolEnergyCostHourly:
            self.pooltotalEnergyCost += hourlyCost
        for hourlyUse in self.poolEnergyUseHourly:
            self.pooltotalEnergyUse += hourlyUse


class Household:
    #these stats not used
    stat_use_of_ev = [False]*24
    stat_use_of_dishwasher = [False] * 24
    stat_use_of_clothdryer = [False] * 24
    stat_use_of_washingmachine = [False]*24



    def __init__(self):
        # on init, run random assignment of appliances
        self.wakeup_hour = random.randint(4, 11)
        self.nighttime = random.randint(20, 23)

        self.totalEnergyCost = 0
        self.totalEnergyUse = 0
        self.energyCostHourly = [0] * 24
        self.energyUseHourly = [0] * 24

        self.timeslots = []
        self.viableTimeslots = findGoodTimeslots(daysPrice.prices, list(range(self.wakeup_hour, self.nighttime)))

        # shiftableAppliances, bool for EV,
        # scheduledAppliances, bool for extra freezer
        # randomAppliances, bool for all
        self.shift_appliances = [boolroll(40)] + [True for x in range(len(shiftableAppliances) - 1)]
        self.nonshift_appliances = [boolroll(20)] + [True for x in range(len(nonshiftableAppliances)-1)]
        self.extra_appliances = [boolroll(60) for x in range(len(extraAppliances))]

        # fill shiftable timeslot
        for index, hasItem in enumerate(self.shift_appliances):
            if hasItem:
                # treat electric car seperatelu
                if index == 0:
                    # spread use across the night for ev
                    hours_of_use = len(evTimeslots)
                    hourly_power_use = shiftAppPower[index] / hours_of_use
                    for hour in evTimeslots:
                        price_of_use = daysPrice.prices[hour] * (hourly_power_use/1000)
                        self.energyCostHourly[hour] += price_of_use
                        self.energyUseHourly[hour] += hourly_power_use
                # Other shiftable appliances
                elif index != 0:
                    rand_index = random.randint(0, len(self.viableTimeslots) - 1)
                    chosenTimeslot = self.viableTimeslots[rand_index]
                    price_of_use = daysPrice.prices[chosenTimeslot] * (shiftAppPower[index] / 1000)
                    self.energyCostHourly[chosenTimeslot] += price_of_use
                    self.energyUseHourly[chosenTimeslot] += shiftAppPower[index]

        # fill non-shiftable timeslots
        for index, hasItem in enumerate(self.nonshift_appliances):
            #if the household has this appliance
            if hasItem:
                #0,1,2,3,: "heating", "Refridgeration", "water heater", spread across all day
                if index in range(4):
                    #spread use across the day for certain appliances
                    hourly_power_use = nonshiftAppPower[index] / 24
                    for hour, price in enumerate(daysPrice.prices):
                        price_of_use = price * (hourly_power_use / 1000)
                        self.energyCostHourly[hour] += price_of_use
                        self.energyUseHourly[hour] += hourly_power_use

                # other non-shift appliances: once between wakeup and night
                elif index in range(4, 7):
                    rand_index = random.randint(self.wakeup_hour, self.nighttime)
                    price_of_use = daysPrice.prices[rand_index] * (nonshiftAppPower[index] / 1000)
                    self.energyCostHourly[rand_index] += price_of_use
                    self.energyUseHourly[rand_index] += nonshiftAppPower[index]

                # lighting: spread between wakeup and night
                if index >= 7:
                    # spread use across the day for lighting
                    hours_of_use = self.nighttime - self.wakeup_hour
                    hourly_power_use = nonshiftAppPower[index] / hours_of_use
                    for basehour, price in enumerate(daysPrice.prices[self.wakeup_hour:self.nighttime]):
                        price_of_use = price * (hourly_power_use / 1000)
                        self.energyCostHourly[basehour+self.wakeup_hour] += price_of_use
                        self.energyUseHourly[basehour+self.wakeup_hour] += hourly_power_use

        # fill extra items timeslots
        for index, hasItem in enumerate(self.extra_appliances):
            if hasItem:
                rand_index = random.randint(0, 23)
                price_of_use = daysPrice.prices[rand_index] * (extraAppPower[index] / 1000)
                self.energyCostHourly[rand_index] += price_of_use
                self.energyUseHourly[rand_index] += extraAppPower[index]

        #statistics at end
        for hourly_cost in self.energyCostHourly:
            self.totalEnergyCost += hourly_cost
        for hourly_power in self.energyUseHourly:
            self.totalEnergyUse += hourly_power

class DailyPricing:
    def __init__(self, dayMin, dayMax):
        self.dayMax = dayMax
        self.dayMin = dayMin
        self.timeTeller = 24
        self.prices = [0] * self.timeTeller
        for index in range(self.timeTeller):
            self.prices[index] = random.randint(self.dayMin, self.dayMax - 20)
        peakhour = random.randint(8, 20)
        self.prices[peakhour:peakhour + 3] = [random.randint(self.dayMax - 20, self.dayMax),
                                              random.randint(self.dayMax - 20, self.dayMax),
                                              random.randint(self.dayMax - 20, self.dayMax)]

        self.prices = [50, 35, 46, 47, 26, 37, 22, 34, 46, 39, 36, 47, 65, 60, 60, 36, 21, 23, 40, 26, 38, 27, 38, 44]

def findGoodTimeslots(myprices, available_hours):
    # three strategies = disregard energy cost, avoid tops, seek out bottoms
    timeslot_price = []
    for hour in available_hours:
        timeslot_price.append(myprices[hour])

    #strategies a household can use to lower electricity cost:
    #choose one of these in the price comparison 10~ lines down.
    high_percentile = np.percentile(timeslot_price, 80)
    low_percentile = np.percentile(timeslot_price, 20)
    all_percentile = np.percentile(timeslot_price, 100)
    mid_percentile = np.percentile(timeslot_price, 50)

    timeslots = []
    for index, price in enumerate(myprices):
        # TODO change price comparison for different strategies.
        if index in available_hours:
            if price < high_percentile:
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


shiftableAppliances = ["Electric Vehicle", "Dishwasher", "Laundry Machine", "Cloth Dryer"]
shiftAppPower = [9900, 1440, 1940, 2500]
nonshiftableAppliances = ["separate freezer", "Heating", "Refrigeration",
                          "water heater", "Electric stove", "TV", "Computer"] \
                         + ["Lighting"] * 10
nonshiftAppPower = [2000, 6000, 3000, 2000, 1000, 600, 400] + [100] * 10
extraAppliances = ["coffee maker", "ceiling fan", "hair dryer", "toaster", "modem",
                   "microwave", "router", "cellphone charger", "cloth iron", "fan",
                   "laptop", "e-bike", "e-scooter", "wheelchair", "elevator",
                   "playstation", "radio", "cd player", "lawn mover", "vacuum cleaner"]
extraAppPower = [100, 300, 100, 100, 50,
                 300, 100, 100, 100, 200,
                 200, 500, 400, 500, 1000,
                 200, 50, 50, 400, 200]

print_hi('PyCharm')
daysPrice = DailyPricing(20, 80)
print(daysPrice.prices)

bestTimeslots = findGoodTimeslots(daysPrice.prices, list(range(24)))
evTimeslots = findGoodTimeslots(daysPrice.prices, list(range(7)) + list(range(18, 24)))
print(bestTimeslots)

houses = [Household() for x in range(30)]
myNeighbourhood = Neighbourhood(houses)

print(myNeighbourhood.poolEnergyUseHourly)
print(myNeighbourhood.poolEnergyCostHourly)
print("avg home uses ", myNeighbourhood.pooltotalEnergyCost / 30 / 100, "kr")

energycostbyhouse=[]
for house in myNeighbourhood.households:
    energycostbyhouse.append(house.totalEnergyCost)
print(energycostbyhouse)

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Neighbourhood energy use vs cost of energy in øre/kwh')
ax1.plot(list(range(24)), [x/(1000) for x in myNeighbourhood.poolEnergyUseHourly], label="Energy usage")
ax2.plot(list(range(24)), daysPrice.prices, label="cost øre/KWT")
ax1.set_ylabel("kwh")
ax2.set_ylabel("øre/kwh")
ax2.set_xlabel("hour of day")
plt.show()
