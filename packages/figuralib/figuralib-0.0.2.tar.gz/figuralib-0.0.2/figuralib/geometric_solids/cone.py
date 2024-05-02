def volume(r, h):
    return (1/3) * 3.14159 * r**2 * h

def surface_area(r, h):
    slant_height = (r**2 + h**2)**0.5
    return 3.14159 * r * (r + slant_height)

def lateral_area(r, h):
    slant_height = (r**2 + h**2)**0.5
    return 3.14159 * r * slant_height

def base_area(r):
    return 3.14159 * r**2

def slant_height(r, h):
    return ((r**2) + (h**2))**0.5

def surface_area_with_slant_height(r, slant_height):
    return 3.14159 * r * (r + slant_height)

def volume_with_slant_height(r, slant_height):
    return (1/3) * 3.14159 * r**2 * (slant_height - r)

def lateral_area_with_slant_height(r, slant_height):
    return 3.14159 * r * slant_height

def half_angle(r, h):
    return r / h

def half_angle_degrees(r, h):
    return (r / h) * 180 / 3.14159
