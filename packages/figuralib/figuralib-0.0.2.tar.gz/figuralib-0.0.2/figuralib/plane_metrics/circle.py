pi = 3.14159

def circumference(radius):
    return 2 * radius * pi

def area(radius):
    return radius**2 * pi

def diameter(radius):
    return 2 * radius

def radius(diameter):
    return diameter / 2

def arc_length(radius, angle):
    return radius * angle

def sector_area(radius, angle):
    return (radius**2 * angle) / 2

def inscribed_angle(arc_length, radius):
    return arc_length / radius

def central_angle(arc_length, radius):
    return arc_length / radius

def sector_radius(area, angle):
    return (2 * area / angle) ** 0.5

def sector_angle(area, radius):
    return (2 * area) / (radius**2)

def arc_angle(arc_length, radius):
    return arc_length / radius

def segment_area(radius, chord_length):
    return (radius**2 / 2) * ((chord_length / (2 * radius)))

