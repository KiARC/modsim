from matplotlib import pyplot as plt
from modsim import State, System, TimeFrame, decorate


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
    frame = TimeFrame(columns=system.init.index)
    frame.loc[0] = system.init

    for t in range(0, system.t_end):
        frame.loc[t + 1] = update_func(frame.loc[t], system)

    return frame


def plot_results(data):
    data.s.plot(label='Susceptible')
    data.i.plot(label='Infected')
    data.r.plot(label='Resistant')
    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')
    plt.show()


def add_immunization(system, fraction):
    system.init.s -= fraction
    system.init.r += fraction


# Config
initial_conditions = State(s=600, i=3, r=0)
beta = 1 / 3
gamma = 1 / 4

# Main
system = make_system(beta, gamma, initial_conditions)
results = run_simulation(system, update_func)

system2 = make_system(beta, gamma, initial_conditions)
add_immunization(system2, 0.1)
results2 = run_simulation(system2, update_func)

plot_results(results)
plot_results(results2)