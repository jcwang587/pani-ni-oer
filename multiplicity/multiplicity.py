from pymatgen.io.vasp import Poscar
from pymatgen import MPRester
from pymatgen.electronic_structure.core import Spin

# Load the POSCAR file
poscar = Poscar.from_file("POSCAR")
structure = poscar.structure

# Initialize the Materials Project RESTer
mpr = MPRester("YOUR_API_KEY")  # Replace with your Materials Project API key


# Function to estimate unpaired electrons
def estimate_unpaired_electrons(structure, mpr):
    unpaired_electrons = 0
    for element in structure.composition.elements:
        # Get the electronic structure of the element
        data = mpr.get_data(element.symbol)
        if data:
            electronic_structure = data[0]["electronic_structure"]
            for orbital in electronic_structure[Spin.up]:
                # Simple estimation: if there's an odd number of electrons in an orbital, assume one is unpaired
                if orbital[1] % 2 != 0:
                    unpaired_electrons += 1
    return unpaired_electrons


# Estimate the number of unpaired electrons
unpaired_electrons = estimate_unpaired_electrons(structure, mpr)

# Calculate the multiplicity
multiplicity = unpaired_electrons + 1

print("Estimated number of unpaired electrons:", unpaired_electrons)
print("Estimated multiplicity:", multiplicity)
