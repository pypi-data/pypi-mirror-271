def inertia(mass, velocity):
    return mass * velocity

def impulse(force, time):
    return force * time

def kinetic_energy(mass, velocity):
    return 0.5 * mass * (velocity ** 2)

def velocity(momentum, mass):
    return momentum / mass

def collision_velocity(m1, m2, u1, u2):
    return ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)

def recoil_velocity(m1, m2, u1):
    return u1 * (m1 - m2) / (m1 + m2)
