def perimeter(side_lengths):
    return sum(side_lengths)

def interior_angle(n):
    return (n - 2) * 180 / n

def apothem(s, n):
    return s / (2 * 3.14159 / n)

def area(perimeter, apothem):
    return perimeter * apothem / 2

def side_length(perimeter, num_sides):
    return perimeter / num_sides

def exterior_angle(n):
    return 360 / n

def diagonal(num_sides):
    return num_sides * (num_sides - 3) / 2
