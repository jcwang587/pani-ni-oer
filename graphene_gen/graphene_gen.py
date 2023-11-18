from ase.build import graphene
from ase.io import write

# Create graphene structure
struct = graphene(size=(7, 6, 1))

# Set a small but non-zero lattice vector in the z-direction
struct.cell[2, 2] = 15.0  # Setting the z-component of the lattice vector to 15 Å

# Set periodic boundary conditions in all directions
struct.pbc = [True, True, True]

# Export to CIF file
write('graphene_structure.cif', struct)
