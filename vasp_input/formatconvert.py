from pymatgen.core import Structure

struct = Structure.from_file('CONTCAR2.cif')

# export the structure to a POSCAR file
struct.to(filename='POSCAR', fmt='poscar')