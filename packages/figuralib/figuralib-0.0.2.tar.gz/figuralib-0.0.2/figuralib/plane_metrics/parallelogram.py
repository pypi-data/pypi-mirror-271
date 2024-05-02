def area(base, height):
    return base * height

def perimeter(side1, side2):
    return 2 * (side1 + side2)

def diagonal(side1, side2, angle):
    angle_rad = angle * 0.0174533
    return (side1**2 + side2**2 + 2 * side1 * side2 * (1 - angle_rad**2))**0.5

def height(area, base):
    return area / base

def side_from_area(area, height):
    return area / height

def side_from_perimeter(perimeter, other_side):
    return (perimeter - 2 * other_side) / 2

def angle_between_diagonals(diagonal1, diagonal2, side1, side2):
    cos_angle = (side1**2 + side2**2 - diagonal1**2 - diagonal2**2) / (-2 * diagonal1 * diagonal2)
    if cos_angle <= -1:
        return 180.0
    elif cos_angle >= 1:
        return 0.0
    else:
        angle_rad = acos_safe(cos_angle)
        return angle_rad * 57.2958

def acos_safe(x):
    if x <= -1:
        return 3.14159
    elif x >= 1:
        return 0.0
    else:
        a = x
        b = 1
        while abs(b - a) > 0.00001:
            a = (a + b) / 2
            b = x / sin(a)
        return a

def sin(x):
    return x - x**3 / 6 + x**5 / 120 - x**7 / 5040
