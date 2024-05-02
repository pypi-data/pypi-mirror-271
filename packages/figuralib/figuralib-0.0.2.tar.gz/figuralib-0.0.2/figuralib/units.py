milimetres = "mm"
square_milimetres = "mm²"
cubic_milimetres = "mm³"

centimetres = "cm"
square_centimetres = "cm²"
cubic_centimetres = "cm³"

decimetres = "dm"
square_decimetres = "dm²"
cubic_decimetres = "dm³"

metres = "m"
square_metres = "m²"
cubic_metres = "m³"

kilometres = "km"
square_kilometres = "km²"
cubic_kilometres = "km³"

grams = "g"
litres = "l"

########################################################################################################################

def milimetres_to_centimetres(mm):
	return mm / 10

def centimetres_to_decimetres(cm):
	return cm / 10

def decimetres_to_metres(dm):
	return dm / 10

def metres_to_kilometres(m):
	return m / 10

def centimetres_to_milimetres(cm):
	return cm * 10

def decimetres_to_centimetres(dm):
	return dm * 10

def metres_to_decimetres(m):
	return m * 10

def kilometres_to_metres(km):
	return km * 10

########################################################################################################################

def square_mm_to_square_cm(square_mm):
	return square_mm / 100

def square_cm_to_square_dm(square_cm):
	return square_cm / 100

def square_dm_to_square_m(square_dm):
	return square_dm / 100

def square_m_to_square_km(square_m):
	return square_m / 100

def square_cm_to_square_mm(square_cm):
	return square_cm * 100

def square_dm_to_square_cm(square_dm):
	return square_dm * 100

def square_m_to_square_dm(square_m):
	return square_m * 100

def square_km_to_square_m(square_km):
	return square_km * 100

########################################################################################################################

def cubic_mm_to_cubic_cm(cubic_mm):
	return cubic_mm / 1000

def cubic_cm_to_cubic_dm(cubic_cm):
	return cubic_cm / 1000

def cubic_dm_to_cubic_m(cubic_dm):
	return cubic_dm / 1000

def cubic_m_to_cubic_km(cubic_m):
	return cubic_m / 1000

def cubic_cm_to_cubic_mm(cubic_cm):
	return cubic_cm * 1000

def cubic_dm_to_cubic_cm(cubic_dm):
	return cubic_dm * 1000

def cubic_m_to_cubic_dm(cubic_m):
	return cubic_m * 1000

def cubic_km_to_cubic_m(cubic_km):
	return cubic_km * 1000