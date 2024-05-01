def perimeter(length, width):
    return 2 * (length + width)

def area(length, width):
    return length * width

def diagonal_length(length, width):
    return (length ** 2 + width ** 2) ** 0.5

def is_square(length, width):
    return length == width

def is_golden_rectangle(length, width):
    golden_ratio = (1 + (5 ** 0.5)) / 2
    return length / width == golden_ratio or width / length == golden_ratio

def interior_angle(angle1, angle2):
    return 180 - angle1 - angle2

def is_regular(length, width):
    return length == width

def is_oblong(length, width):
    return length > width
