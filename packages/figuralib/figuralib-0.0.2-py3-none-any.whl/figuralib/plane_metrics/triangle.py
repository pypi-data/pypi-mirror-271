def perimeter(side1, side2, side3):
    return side1 + side2 + side3

def area(base, height):
    return 0.5 * base * height

def is_equilateral(side1, side2, side3):
    return side1 == side2 == side3

def is_isosceles(side1, side2, side3):
    return side1 == side2 or side1 == side3 or side2 == side3

def is_scalene(side1, side2, side3):
    return side1 != side2 != side3

def is_right(angle1, angle2, angle3):
    return angle1 == 90 or angle2 == 90 or angle3 == 90

def is_acute(angle1, angle2, angle3):
    return angle1 < 90 and angle2 < 90 and angle3 < 90

def is_obtuse(angle1, angle2, angle3):
    return angle1 > 90 or angle2 > 90 or angle3 > 90

def height(side1, side2, side3):
    s = perimeter(side1, side2, side3) / 2
    return (2 / side1) * ((s * (s - side2) * (s - side3)) ** 0.5)

def semiperimeter(side1, side2, side3):
    return perimeter(side1, side2, side3) / 2
