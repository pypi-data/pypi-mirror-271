def volume(major_radius, minor_radius):
    return 2 * 3.14159 ** 2 * major_radius * minor_radius ** 2

def surface_area(major_radius, minor_radius):
    return 4 * 3.14159 ** 2 * major_radius * minor_radius

def major_circumference(major_radius):
    return 2 * 3.14159 * major_radius

def minor_circumference(minor_radius):
    return 2 * 3.14159 * minor_radius

def mean_radius(major_radius, minor_radius):
    return (2 * major_radius + minor_radius) / 2

def cross_sectional_area(minor_radius):
    return 3.14159 * minor_radius ** 2

def ring_volume(major_radius, minor_radius):
    return 2 * 3.14159 * major_radius * minor_radius ** 2

def ring_surface_area(major_radius, minor_radius):
    return 4 * 3.14159 * major_radius * minor_radius

def inner_radius(major_radius, minor_radius):
    return major_radius - minor_radius

def inner_circumference(major_radius, minor_radius):
    return 2 * 3.14159 * (major_radius - minor_radius)
