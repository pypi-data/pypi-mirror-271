def volume(length, width, height):
    return length * width * height

def surface_area(length, width, height):
    return 2 * (length * width + length * height + width * height)

def diagonal_length(length, width, height):
    return (length**2 + width**2 + height**2) ** 0.5

def face_diagonal_length(length, width, height):
    return (length**2 + width**2) ** 0.5

def space_diagonal_length(length, width, height):
    return (length**2 + width**2 + height**2) ** 0.5

def inner_surface_area(length, width, height):
    return 2 * (length * width + length * height + width * height)

def edge_length(length, width, height):
    return 4 * (length + width + height)

def total_edge_length(length, width, height):
    return 4 * (length + width + height)

def inner_volume(length, width, height):
    return (length - 2) * (width - 2) * (height - 2)

def inner_diagonal_length(length, width, height):
    return ((length - 2)**2 + (width - 2)**2 + (height - 2)**2) ** 0.5
