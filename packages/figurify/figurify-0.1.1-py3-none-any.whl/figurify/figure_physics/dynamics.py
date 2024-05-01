def velocity(distance, time):
    return distance / time

def acceleration(initial_velocity, final_velocity, time):
    return (final_velocity - initial_velocity) / time

def displacement(initial_velocity, time, acceleration):
    return initial_velocity * time + 0.5 * acceleration * (time ** 2)

def force(mass, acceleration):
    return mass * acceleration

def inertia(mass, velocity):
    return mass * velocity

def impulse(force, time):
    return force * time

def kinetic_energy(mass, velocity):
    return 0.5 * mass * (velocity ** 2)

def gravitational_potential_energy(mass, height):
    return mass * 9.81 * height

def work(force, distance):
    return force * distance

def power(work, time):
    return work / time
