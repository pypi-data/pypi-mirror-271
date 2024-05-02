def volume(base_area, height):
    return (1/3) * base_area * height

def surface_area(base_perimeter, slant_height):
    return 0.5 * base_perimeter * slant_height + base_area(base_perimeter, apothem(base_perimeter, slant_height))

def lateral_area(base_perimeter, slant_height):
    return 0.5 * base_perimeter * slant_height

def base_area(base_perimeter, base_apothem):
    return 0.5 * base_perimeter * base_apothem

def total_area(base_perimeter, slant_height):
    return 0.5 * base_perimeter * (base_perimeter + 2 * slant_height)

def apothem(base_side_length, height):
    return (base_side_length**2 - (0.5*height)**2)**0.5

def surface_area_with_apothem(base_perimeter, apothem):
    return 0.5 * base_perimeter * (apothem + (base_perimeter**2 + 4*apothem**2)**0.5)

def total_area_with_apothem(base_perimeter, apothem):
    return 0.5 * base_perimeter * (base_perimeter + (base_perimeter**2 + 4*apothem**2)**0.5)

def slant_height(base_side_length, height):
    return (base_side_length**2 + height**2)**0.5

def total_edge_length(base_side_length):
    return 4 * base_side_length

def inner_surface_area(base_perimeter, height):
    return base_perimeter * height + base_area(base_perimeter, apothem(base_perimeter, height))

def inner_volume(base_area, height):
    return (1/3) * base_area * height

def inner_diagonal_length(base_side_length, height):
    return ((base_side_length / 2)**2 + height**2)**0.5
