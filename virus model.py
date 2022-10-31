from matplotlib import pyplot as plt
from modsim import State, System, TimeSeries, decorate


# Functions
def make_system(beta, gamma, init):
    init /= init.sum()
    return System(init=init, t_end=7 * 14, beta=beta, gamma=gamma)


def update_func(state, system):
    s, i, r = state.s, state.i, state.r
    infected = system.beta * i * s
    recovered = system.gamma * i
    s -= infected
    i += infected - recovered
    r += recovered
    return State(s=s, i=i, r=r)


def run_simulation(system, update_func):
    s = TimeSeries()
    i = TimeSeries()
    r = TimeSeries()

    state = system.init
    s[0], i[0], r[0] = state
    for t in range(0, system.t_end):
        state = update_func(state, system)
        s[t + 1], i[t + 1], r[t + 1] = state.s, state.i, state.r
    return s, i, r


def plot_results(s, i, r):
    s.plot(label='Susceptible')
    i.plot(label='Infected')
    r.plot(label='Resistant')
    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')
    plt.show()


# Config
initial_conditions = State(s=600, i=3, r=0)
beta = 1 / 3
gamma = 1 / 4

# Main
system = make_system(beta, gamma, initial_conditions)
s, i, r = run_simulation(system, update_func)
plot_results(s, i, r)
