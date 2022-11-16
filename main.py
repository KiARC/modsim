from modsim import System, TimeSeries, decorate, plt


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
    system.t -= system.r * (system.t - system.t_env)


def simulate(system, t_end, offset=0):
    time_series = TimeSeries()
    time_series[offset] = system.t
    for i in range(offset + 1, t_end+offset):
        update(system)
        time_series[i] = system.t
    return time_series


def plot(*sets):
    for set in sets:
        ts, label = set
        ts.plot(label=label)
    decorate(xlabel='Time (minutes)',
             ylabel='Degrees Celsius')
    plt.show()


# Config
coffee = System(t=90, r=0.01, v=350)
milk = System(t=5, r=0.061086056, v=50)
t_env = 30
mix_point= 15

coffeeSys = setup_system(coffee, t_env)
milkSys = setup_system(milk, t_env)
coffeeSim = simulate(coffeeSys, mix_point)
milkSim = simulate(milkSys, mix_point)
mix = mix(coffee, milk)
mixSys = setup_system(mix, t_env)
mixSim = simulate(mixSys, mix_point, mix_point)

plot((mixSim, "Mix"), (coffeeSim, "Coffee"), (milkSim, "Milk"))