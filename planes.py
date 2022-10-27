from modsim import  *
from random import randint

# Constants (Start, Dest, volume, time)
planes = State(Miami=28, Dulles=40, Design=50)

capacities = {
    "Miami": 28,
    "Dulles": 40,
    "Design": 50
}

late = {
    "Miami": 0,
    "Dulles": 0,
    "Design": 0
}

from_to = {
    "Dulles": 16,
    "Design": 20,
    "Miami": 24
}

hours = {
    "Miami": {
        "Dulles":2,
        "Design": 4
    },
    "Dulles": {
        "Miami": 2,
        "Design": 6
    },
    "Design": {
        "Miami": 4,
        "Dulles": 6
    }
}
planes_miami = TimeSeries()
planes_dulles = TimeSeries()
planes_design = TimeSeries()

in_air = []

"""
Does the thing that makes the simulation simulate stuff

p1: probability 1
p2: probability 2
num_steps: number of steps
"""


def run_simulation(steps):
    planes_miami[0] = 12
    planes_dulles[0] = 15
    planes_design[0] = 25
    for i in range(1, steps):
        step()
        planes_miami[i] = planes.Miami
        planes_dulles[i] = planes.Dulles
        planes_design[i] = planes.Design


def takeoff(origin, dest, count, time):
    global in_air
    if planes[origin] < count:
        available = planes[origin] - count
        late[origin] += count - available
        planes[origin] -= available
        for _ in range(available):
            in_air.append([dest, time])
    else:
        planes[origin] -= count
        for _ in range(count):
            in_air.append([dest, time])
    return in_air


"""
A single step in the simulation

p1: probability 1
p2: probability 2
"""


def step():
    global in_air
    for source in from_to:
        first = randint(0, from_to[source] - 8)
        second = from_to[source] - first
        s = False
        for i in ["Dulles", "Design", "Miami"]:
            if source != i:
                if not s:
                    takeoff(source, i, first, hours[source][i])
                    s = True
                else:
                    takeoff(source, i, second, hours[source][i])
    temp = in_air.copy()
    count = 0
    for i in range(len(temp)):
        j = i - count
        if  temp[j][1] <= 1:
            dest = temp[j][0]
            if (planes[dest] <= capacities[dest]):
                del temp[j]
                count += 1
                planes[dest] += 1
            else:
                late[dest] += 1
        else:
            temp[j][1] -= 1
    in_air = temp.copy()


run_simulation(100)

# Graphy stuff
planes_miami.plot(label="Miami")
planes_dulles.plot(label="Dulles")
planes_design.plot(label="Design")
decorate(title='Planes',
         xlabel='Time step (hr)',
         ylabel='Number of planes per location')
plt.show()

print(
    f"Miami:\n{planes_miami}\nDulles:\n{planes_dulles}\nDesign:\n{planes_design}")
late_miami = late["Miami"]
late_dulles = late["Dulles"]
late_design = late["Design"]
plt.bar(["Miami", "Dulles", "Design"], [late_miami, late_dulles, late_design], color=["red", "green", "blue"], width=1)
plt.xlabel("Airport")
plt.ylabel("Hours late")
plt.title("Number of hours worth of late time")
plt.show()