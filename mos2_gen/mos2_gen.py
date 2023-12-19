from ase.build import mx2
from ase.io import write

# MoS2 unit cell dimensions
mos2_size_x = 7
mos2_size_y = 4

# Create MoS2 structure
mos2_struct = mx2(formula='MoS2', kind='2H', size=(mos2_size_x, mos2_size_y, 1), vacuum=15.0)
mos2_struct.translate([0, 0, 5.0])
mos2_struct.pbc = [True, True, True]

# Export to CIF file
write('mos2_structure.cif', mos2_struct)
