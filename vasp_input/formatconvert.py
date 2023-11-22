from pymatgen.core import Structure

struct = Structure.from_file('CONTCAR')

# export structure to cif file
struct.to(filename='CONTCAR.cif')