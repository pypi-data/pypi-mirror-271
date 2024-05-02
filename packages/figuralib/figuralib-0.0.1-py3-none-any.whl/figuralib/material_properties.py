def density(mass, volume):
    return mass / volume

def mass(density, volume):
    return density * volume

def volume(mass, density):
    return mass / density

def flexibility(elastic_modulus, geometry_factor):
    return elastic_modulus / geometry_factor

def strength(structural_factor, composition_factor):
    return structural_factor * composition_factor

def melting_point(heat_capacity, heat_transfer_rate):
    return heat_capacity / heat_transfer_rate

def boiling_point(vapor_pressure, atmospheric_pressure):
    return vapor_pressure / atmospheric_pressure

def conductivity(thermal_conductivity, cross_sectional_area, temperature_gradient):
    return thermal_conductivity * cross_sectional_area * temperature_gradient

def refractive_index(speed_of_light, wavelength):
    return speed_of_light / wavelength
