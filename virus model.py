from matplotlib import pyplot as plt
from modsim import State, SweepFrame, SweepSeries, System, TimeFrame, contour, decorate, linspace


# Functions
def make_system(beta, gamma, qrate, init):
    init /= init.sum()
    return System(init=init, t_end=7 * 14, beta=beta, gamma=gamma, qrate=qrate)


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
    data.q.plot(label="Quarantined")
    decorate(xlabel='Time (days)',
             ylabel='Fraction of population')
    plt.show()


def add_immunization(system, fraction):
    system.init.s -= fraction
    system.init.r += fraction


def calc_total_infected(results, system):
    s_0 = results.s[0]
    s_end = results.s[system.t_end]
    return s_0 - s_end


def sweep_beta(beta_array, gamma):
    sweep = SweepSeries()
    for beta in beta_array:
        system = make_system(beta, gamma, initial_conditions)
        results = run_simulation(system, update_func)
        sweep[beta] = calc_total_infected(results, system)
    return sweep


def sweep_parameters(beta_array, gamma_array):
    frame = SweepFrame(columns=gamma_array)
    for gamma in gamma_array:
        frame[gamma] = sweep_beta(beta_array, gamma)
    return frame


def plot_sweep_frame(frame):
    for gamma in frame.columns:
        column = frame[gamma]
        for beta in column.index:
            metric = column[beta]
            plt.plot(beta / gamma, metric, '.', color='C1')


def update_quarantining(state, system):
    s, i, r, q = state.s, state.i, state.r, state.q
    infected = system.beta * i * s
    recovered_i = system.gamma * i
    recovered_q = system.gamma * q
    s -= infected
    i += infected - recovered_i
    r += recovered_i + recovered_q
    quarantined = system.qrate * i
    i -= quarantined
    q += quarantined - recovered_q
    return State(s=s, i=i, r=r, q=q)


# Config
initial_conditions = State(s=600, i=3, r=0, q=0)
beta = 1 / 3
gamma = 1 / 4
"""qrate=0
"""
qrate = 1/10
"""
# Main """
results = run_simulation(
    make_system(
        beta,
        gamma,
        qrate,
        initial_conditions
    ),
    update_quarantining
)
plot_results(results)