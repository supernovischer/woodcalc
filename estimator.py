def calculate_mass(count, diameter_cm, length_m, density_kg_m3):
    """
    Calculates the estimated mass of the piles.
    
    Args:
        count (int): Number of piles.
        diameter_cm (float): Average diameter of a pile in cm.
        length_m (float): Average length of a pile in meters.
        density_kg_m3 (float): Density of the wood in kg/m^3.
        
    Returns:
        float: Estimated total mass in kg.
    """
    radius_m = (diameter_cm / 100) / 2
    volume_per_pile_m3 = 3.14159 * (radius_m ** 2) * length_m
    total_volume = count * volume_per_pile_m3
    total_mass = total_volume * density_kg_m3
    return total_mass
