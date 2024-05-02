def volume(radius):
    return (4/3) * 3.14159 * radius ** 3

def surface_area(radius):
    return 4 * 3.14159 * radius ** 2

def circumference(radius):
    return 2 * 3.14159 * radius

def cross_sectional_area(radius):
    return 3.14159 * radius ** 2

def spherical_cap_volume(radius, depth):
    return (1/3) * 3.14159 * depth**2 * (3 * radius - depth)

def spherical_cap_surface_area(radius, depth):
    return 2 * 3.14159 * radius * depth

def spherical_sector_volume(radius, angle):
    return (2/3) * 3.14159 * radius ** 3 * angle

def spherical_sector_surface_area(radius, angle):
    return 2 * 3.14159 * radius ** 2 * (1 + ((1 - angle**2 / 2) + (1 - angle**4 / 8) + (1 - angle**6 / 48)))

def chord_length(radius, angle):
    return 2 * radius * (angle / 2)

def great_circle_distance(radius, angle):
    return radius * (angle / 180)
