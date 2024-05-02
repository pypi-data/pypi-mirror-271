def force(mass, acceleration):
    return mass * acceleration

def weight(mass):
    return mass * 9.81

def tension(angle, mass):
    return mass * 9.81 / angle

def friction_coefficient(friction_force, normal_force):
    return friction_force / normal_force

def gravitational_force(mass1, mass2, distance):
    return 6.674 * (10 ** -11) * (mass1 * mass2) / (distance ** 2)

def spring_force(spring_constant, displacement):
    return spring_constant * displacement

def buoyant_force(density, volume, gravity):
    return density * volume * gravity

def magnetic_force(charge1, charge2, distance):
    return (9 * (10 ** 9)) * (charge1 * charge2) / (distance ** 2)
