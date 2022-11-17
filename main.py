from modsim import System, TimeSeries, decorate, plt


def mix(*systems):
    a = 0
    # Mix Temperatures
    for system in systems:
        a += system.v * system.t
    total_volume = 0
    for system in systems:  # Calculate total volume
        total_volume += system.v
    temperature = a / total_volume
    # Mix r values
    r = 0
    for system in systems:
        r += system.v * system.r
    r /= total_volume
    # Mix t_env, but they should be the same really
    t_env = 0
    for system in systems:
        t_env += system.v * system.t_env
    t_env /= total_volume
    return System(t=temperature, v=total_volume, r=r, t_env=t_env)


def update(system):
    system.t -= system.r * (system.t - system.t_env)


def simulate(system, t_end, offset=0):
    time_series = TimeSeries()
    time_series[offset] = system.t
    for i in range(offset + 1, t_end + offset):
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
coffee = System(t=90, r=0.01, v=350, t_env=30)  # Define coffee system
milk = System(t=5, r=0.061086056, v=50, t_env=30)  # Define milk system
t_env = 30  # Define ambient temperature
mix_point = 15  # Define the point at which the systems are mixed

coffeeSim = simulate(coffee, mix_point)  # Simulate coffee to the mix point
milkSim = simulate(milk, mix_point)  # Simulate milk to the mix point
mix = mix(coffee, milk)  # Mix systems together
mixSim = simulate(mix, mix_point, mix_point)  # Simulate mix for the same amount of time, starting at the mix_point

plot((mixSim, "Mix"), (coffeeSim, "Coffee"), (milkSim, "Milk"))  # Plot results
mixSim = simulate(mixSys, mix_point, mix_point)

plot((mixSim, "Mix"), (coffeeSim, "Coffee"), (milkSim, "Milk"))