def gravitational_force(mass1, mass2, distance):
    return 6.674 * (10 ** -11) * (mass1 * mass2) / (distance * distance)

def gravitational_acceleration(mass, distance):
    return 6.674 * (10 ** -11) * (mass) / (distance * distance)

def gravitational_potential_energy(mass1, mass2, distance):
    return (-6.674 * (10 ** -11) * (mass1 * mass2)) / distance

def escape_velocity(mass, radius):
    return 2 * 6.674 * (10 ** -11) * mass / radius

def orbital_period(semi_major_axis, mass):
    return 2 * 3.14159 * (semi_major_axis ** 1.5) / (6.674 * (10 ** -11) * mass)
