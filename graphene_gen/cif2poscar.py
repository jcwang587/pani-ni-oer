from pymatgen.core import Structure

cif_file = 'graphene_structure_ms.cif'
cif = Structure.from_file(cif_file)

# export to POSCAR
cif.to(filename='POSCAR', fmt='poscar')
