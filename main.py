from modsim import System, TimeSeries


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
    return System(temperature, total_volume, r)


def update(system, t_env):
    system.t = system.r * (system.t - t_env)


def simulate(system, t_env, steps):
    time_series = TimeSeries()
    time_series[0] = system.t
    for i in range(1, steps):
        update(system, t_env)
        time_series[i] = system.t
    return time_series


coffee = System(t=90, r=0.01, v=350)
milk = System(t=5, r=0.061086056, v=50)
