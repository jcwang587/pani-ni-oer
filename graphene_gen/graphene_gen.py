from ase.build import graphene

struct = graphene(size=(7, 6, 1), vacuum=None)

# export to xyz file
from ase.io import write

write('graphene_structure.xyz', struct)
