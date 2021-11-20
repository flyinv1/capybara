from .units import qty

def hoop(P, r, t):
    """ Get hoop stress from internal pressure, material properties, radius, and wall thickness
    """
    return P * r / (2 * t)
    
def longitudinal(P, r, t):
    """ Get longitudinal stress from internal pressure, material properties, and wall thickness
    """
    return P * r / t

def fos(strength, stress):
    return strength / stress





    