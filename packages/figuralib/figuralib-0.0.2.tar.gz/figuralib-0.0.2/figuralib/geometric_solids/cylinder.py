def volume(radius, height):
    return 3.14159 * radius ** 2 * height

def lateral_area(radius, height):
    return 2 * 3.14159 * radius * height

def surface_area(radius, height):
    return 2 * 3.14159 * radius * (radius + height)

def base_area(radius):
    return 3.14159 * radius ** 2

def curved_surface_area(radius, height):
    return 2 * 3.14159 * radius * height

def total_area(radius, height):
    return 2 * 3.14159 * radius * (radius + height)

def diagonal_length(radius, height):
    return (radius**2 + height**2)**0.5

def lateral_surface_area_with_diagonal(radius, height):
    return 3.14159 * (radius + (radius**2 + height**2)**0.5) * height

def total_area_with_diagonal(radius, height):
    return 3.14159 * (2 * radius * (radius + (radius**2 + height**2)**0.5) + radius**2)
