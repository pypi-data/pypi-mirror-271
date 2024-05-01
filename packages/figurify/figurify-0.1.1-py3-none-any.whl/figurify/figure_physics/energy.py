def kinetic_energy(mass, velocity):
    return 0.5 * mass * (velocity ** 2)

def gravitational_potential_energy(mass, height):
    return mass * 9.81 * height

def elastic_potential_energy(spring_constant, displacement):
    return 0.5 * spring_constant * (displacement ** 2)

def mechanical_energy(kinetic_energy, potential_energy):
    return kinetic_energy + potential_energy

def thermal_energy(mass, specific_heat_capacity, temperature_change):
    return mass * specific_heat_capacity * temperature_change

def electrical_energy(voltage, current, time):
    return voltage * current * time

def sound_energy(sound_intensity, area):
    return sound_intensity * area
