from modsim import System, TimeSeries, plt


def mix(*systems):
    a = 0
    for system in systems:
        a += system.v * system.t
    total_volume = 0
    for system in systems:
        total_volume += system.v
    temperature = a / total_volume
    r = 0
    for system in systems:
        r += system.v * system.r
    r /= total_volume
    return System(t=temperature, v=total_volume, r=r)


def setup_system(system, t_env):
    return System(t=system.t, r=system.r, v=system.v, t_env=t_env)


def update(system):
    system.t = system.r * (system.t - system.t_env)


def simulate(system, t_end):
    time_series = TimeSeries()
    time_series[0] = system.t
    for i in range(1, t_end):
        update(system)
        time_series[i] = system.t
    return time_series


coffee = System(t=90, r=0.01, v=350)
milk = System(t=5, r=0.061086056, v=50)
t_env = 30
steps = 30
ts = simulate(setup_system(mix(coffee, milk), t_env), steps)
ts.plot()
plt.show()
