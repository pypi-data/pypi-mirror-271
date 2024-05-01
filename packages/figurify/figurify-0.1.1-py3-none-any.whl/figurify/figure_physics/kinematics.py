def average_speed(distance, time):
    return distance / time

def average_velocity(displacement, time):
    return displacement / time

def acceleration(initial_velocity, final_velocity, time):
    return (final_velocity - initial_velocity) / time

def final_velocity(initial_velocity, acceleration, time):
    return initial_velocity + acceleration * time

def displacement(initial_velocity, time, acceleration):
    return initial_velocity * time + 0.5 * acceleration * (time ** 2)

def final_velocity_squared(initial_velocity_squared, acceleration, displacement):
    return initial_velocity_squared + 2 * acceleration * displacement