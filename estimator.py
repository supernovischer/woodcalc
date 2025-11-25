def calculate_mass(count, diameter_cm, length_m, density_kg_m3):
    """
    Calculates the estimated mass of the piles (cylindrical).
    """
    radius_m = (diameter_cm / 100) / 2
    volume_per_pile_m3 = 3.14159 * (radius_m ** 2) * length_m
    total_volume = count * volume_per_pile_m3
    total_mass = total_volume * density_kg_m3
    return total_mass

def calculate_mass_rectangular(count, width_cm, height_cm, length_m, density_kg_m3):
    """
    Calculates the estimated mass of boards/beams (cuboid).
    """
    width_m = width_cm / 100
    height_m = height_cm / 100
    volume_per_item_m3 = width_m * height_m * length_m
    total_volume = count * volume_per_item_m3
    total_mass = total_volume * density_kg_m3
    return total_mass
