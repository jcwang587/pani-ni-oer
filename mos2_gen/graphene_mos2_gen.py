from ase.io import write
from ase.build import mx2, graphene

# Create graphene structure
graphene_struct = graphene(size=(9, 9, 1))
graphene_struct.cell[2, 2] = 15.0
graphene_struct.translate([0, 0, 5.0])
graphene_struct.pbc = [True, True, True]

# MoS2 unit cell dimensions
mos2_size_x = 7
mos2_size_y = 4

# Create MoS2 structure
mos2_struct = mx2(formula='MoS2', kind='2H', size=(mos2_size_x, mos2_size_y, 1))
mos2_struct.translate([0, 0, 5.0])
mos2_struct.pbc = [True, True, True]

# Adjust position if necessary (optional)
# For example, translate one of the structures
mos2_struct.translate([0, 0, 5])

# Combine the structures
combined_struct = graphene_struct + mos2_struct

# Export to CIF file
write('combined_structure.cif', combined_struct)
