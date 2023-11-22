from ase.io import read, write

# Read the cif file
struct = read('POSCAR', format='vasp')
# Write the structure to a POSCAR file
struct.write('POSCAR2', format='vasp')