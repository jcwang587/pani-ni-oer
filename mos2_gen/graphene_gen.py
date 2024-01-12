from ase.build import graphene
from ase.io import write

# Create graphene structure
struct = graphene(size=(9, 9, 1))
struct.cell[2, 2] = 15.0
struct.translate([0, 0, 5.0])
struct.pbc = [True, True, True]

# Export to CIF file
write('graphene_structure.cif', struct)
