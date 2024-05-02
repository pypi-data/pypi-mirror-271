def volume(base_area, height):
    return base_area * height

def surface_area(base_perimeter, base_apothem, height):
    return base_perimeter * height + 2 * base_area(base_perimeter, base_apothem)

def lateral_area(base_perimeter, height):
    return base_perimeter * height

def base_area(base_perimeter, base_apothem):
    return 0.5 * base_perimeter * base_apothem

def total_area(base_perimeter, base_apothem, height):
    return base_perimeter * (height + base_apothem) + 2 * base_area(base_perimeter, base_apothem)

def diagonal_length(base_side_length, height):
    return (base_side_length ** 2 + height ** 2) ** 0.5

def lateral_surface_area_with_diagonal(base_side_length, height):
    return base_side_length * (base_side_length + (base_side_length ** 2 + height ** 2) ** 0.5)

def total_area_with_diagonal(base_side_length, height):
    return base_side_length * (2 * base_side_length + (base_side_length ** 2 + height ** 2) ** 0.5) + 2 * base_side_length ** 2
