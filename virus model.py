from modsim import State, System


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


def run_simulation1(system, update_func):
    state = system.init
    for _ in range(0, system.t_end):
        state = update_func(state, system)
    return state


# Config
initial_conditions = State(s=600, i=3, r=0)
beta = 1 / 3
gamma = 1 / 4

# Main
system = make_system(beta, gamma, initial_conditions)
final_state = run_simulation1(system, update_func)
print(final_state)
