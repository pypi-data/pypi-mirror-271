def perimeter(side1, side2, side3, side4):
    return side1 + side2 + side3 + side4

def area(side1, side2, angle):
    height = side2 * angle / 2
    return side1 * height

def diagonal_length(side1, side2, angle):
    return ((side1 ** 2) + (side2 ** 2) - (2 * side1 * side2 * ((1 - (angle / 360)) ** 2))) ** (1/2)

def interior_angle(angle1, angle2):
    return 180 - angle1 - angle2

def semiperimeter(side1, side2, side3, side4):
    return (side1 + side2 + side3 + side4) / 2

def height(area, base):
    return 2 * area / base

def is_parallelogram(angle1, angle2):
    return angle1 == angle2

def is_rhombus(side1, side2, side3, side4):
    return side1 == side2 == side3 == side4

def is_rectangle(angle1, angle2):
    return angle1 == angle2 == 90

def is_square(side1, side2, side3, side4, angle1, angle2):
    return side1 == side2 == side3 == side4 and angle1 == angle2 == 90
