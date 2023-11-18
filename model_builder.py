from ase.io import read
from ase import Atoms
import numpy as np


def remove_edge_hydrogen(structure, H_threshold_distance, random_seed):
    # Set random seed
    np.random.seed(random_seed)

    # Find carbons connected to hydrogen based on distance threshold
    edge_carbons = [atom for atom in structure if atom.symbol == 'C' and
                    any(1 for other in structure if other.symbol == 'H' and
                        np.linalg.norm(atom.position - other.position) <= H_threshold_distance)]
    edge_atom = np.random.choice(edge_carbons)
    edge_atom_coords = edge_atom.position

    # Find the hydrogen atom connected to the edge carbon
    edge_hydrogen = [atom for atom in structure if atom.symbol == 'H' and
                     np.linalg.norm(atom.position - edge_atom_coords) <= H_threshold_distance][0]
    edge_hydrogen_coords = edge_hydrogen.position
    # Remove the hydrogen atom from the structure
    structure.pop(edge_hydrogen.index)

    print("number of edge carbons: ", len(edge_carbons))

    # Return the edge carbon
    return edge_atom_coords, edge_hydrogen_coords


# Set the random seed
random_seed = 102
np.random.seed(random_seed)

# Read the graphene structure
graphene = read('graphene_structure/gaussian_opt_cc_pvdz.pdb')

all_atoms = [atom for atom in graphene]
carbon_atoms = [atom for atom in graphene if atom.symbol == 'C']
all_coords = np.array([atom.position for atom in all_atoms])
carbon_coords = np.array([atom.position for atom in carbon_atoms])

# Get three non-collinear carbon atoms to determine the plane of the graphene
c1 = carbon_coords[0]
c2 = carbon_coords[1]
c3 = carbon_coords[2]

# Calculate two vectors lying in the graphene plane
v1 = c2 - c1
v2 = c3 - c1
normalized_perpendicular = np.cross(v1, v2) / np.linalg.norm(np.cross(v1, v2))

# Set the desired distance between the carbon atom and the attached oxygen atom
CH_distance = 1.1  # typical C-H single bond length in angstroms
CO_distance = 1.43  # typical C-O single bond length in angstroms
C_O_distance = 1.2  # typical C=O double bond length in angstroms
OH_distance = 0.97  # typical O-H bond length in angstroms

# Read the graphene structure
graphene = read('graphene_structure/gaussian_opt_cc_pvdz.pdb')

# Remove the edge hydrogen atom
edge_carbon_position, edge_hydrogen_position = remove_edge_hydrogen(graphene, CH_distance, random_seed)

# Find the direction from the edge carbon to the edge hydrogen
normalized_parallel = ((edge_hydrogen_position - edge_carbon_position) /
                       np.linalg.norm(edge_hydrogen_position - edge_carbon_position))

# Determine the positions for the oxygen atoms
carbonyl_oxygen_position = edge_carbon_position + normalized_parallel * C_O_distance
carbonyl_oxygen_atom = Atoms('O', positions=[carbonyl_oxygen_position])
graphene.extend(carbonyl_oxygen_atom)

# Calculate the distance between each carbon atom and the edge carbon
distance_array = np.zeros((len(carbon_coords), 3))
for i, carbon_atom in enumerate(carbon_atoms):
    distance_array[i, 0] = carbon_atom.index
    distance_array[i, 1] = np.linalg.norm(carbon_atom.position - edge_carbon_position)
    distance_array[i, 2] = np.round(distance_array[i, 1], 0)

# Get the unique distances
distance_values = np.unique(distance_array[:, 2])
distance_values = distance_values[distance_values != 0]

# Randomly select one carbon atom for each distance
select_sites = []
for distance in distance_values:
    select_sites.append(distance_array[distance_array[:, 2] == distance].tolist()[0])

# save the graphene structure with carbonyl oxygen
graphene.write('graphene_structure/graphene_carbonyl.gjf')

# Create a structure for each selected carbon atom
for j, site in enumerate(select_sites):
    graphene_carbonyl = graphene.copy()

    # get the index of the selected carbon atoms
    i_index = int(site[0])
    round_distance = int(site[2])

    # Determine the positions for the oxygen atoms
    oxygen_position_i = all_coords[i_index] + normalized_perpendicular * CO_distance
    hydrogen_position_i = oxygen_position_i + normalized_perpendicular * OH_distance

    # Create and add the oxygen atoms to the structure
    oxygen_atom_i = Atoms('O', positions=[oxygen_position_i])
    hydrogen_atom_i = Atoms('H', positions=[hydrogen_position_i])

    graphene_carbonyl.extend(oxygen_atom_i)
    graphene_carbonyl.extend(hydrogen_atom_i)

    # Write the structure to a gjf file
    filename = 'graphene_structure/graphene_{}.gjf'.format(j + 1)
    graphene_carbonyl.write(filename)

# Create the symmetric structure
graphene_symmetric = graphene.copy()

# Remove the hydrogen atom with index = 37
graphene_symmetric.pop(36)

# Attach -OH to the carbon atom with index = 36
oxygen_position = all_coords[36] - normalized_parallel * CO_distance
hydrogen_position = oxygen_position - normalized_parallel * OH_distance

# Create and add the oxygen atoms to the structure
oxygen_atom = Atoms('O', positions=[oxygen_position])
hydrogen_atom = Atoms('H', positions=[hydrogen_position])

graphene_symmetric.extend(oxygen_atom)
graphene_symmetric.extend(hydrogen_atom)

# Write the structure to a gjf file
graphene_symmetric.write('graphene_structure/graphene_symmetric.gjf')