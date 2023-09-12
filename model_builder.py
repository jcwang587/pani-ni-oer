from ase.io import read
from ase import Atoms
import numpy as np
from scipy.spatial.distance import pdist, squareform


def remove_edge_hydrogen(structure, H_threshold_distance, random_seed=215):
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

    # Return the edge carbon
    return edge_atom_coords, edge_hydrogen_coords


# Set the random seed
np.random.seed(215)

# Read the graphene structure
graphene = read('graphene_structure/gaussian_opt_cc_pvdz.pdb')

# Extract the coordinates of carbon atoms
carbon_coords = [atom.position for atom in graphene if atom.symbol == 'C']

# Calculate the pairwise distances between carbon atoms
distances = pdist(carbon_coords)

# Convert the condensed distance matrix to a square distance matrix
square_distances = squareform(distances)

# Get the upper triangle indices (excluding the diagonal)
i_indices, j_indices = np.triu_indices(len(carbon_coords), k=1)

# Extract the distances using the upper triangle indices
extracted_distances = square_distances[i_indices, j_indices]

# Stack the indices and distances together to form the 3-column array
distance_array = np.column_stack((i_indices, j_indices, extracted_distances))

# Add the round distances to the fourth column
distance_array = np.column_stack((distance_array, np.round(extracted_distances)))
distance_values = np.unique(distance_array[:, 3])

select_sites = []
for distance in distance_values:
    # Select the sites that have the same distance
    i_sites = distance_array[distance_array[:, 3] == distance]
    # randomly select one site from the selected sites
    select_site = i_sites[np.random.randint(len(i_sites))]
    select_sites.append(select_site)
select_sites = np.array(select_sites)

# Get three non-collinear carbon atoms to determine the plane of the graphene
c1 = carbon_coords[0]
c2 = carbon_coords[1]
c3 = carbon_coords[2]

# Calculate two vectors lying in the graphene plane
v1 = c2 - c1
v2 = c3 - c1

# Find the direction perpendicular to the graphene plane using cross product
normalized_perpendicular = np.cross(v1, v2) / np.linalg.norm(np.cross(v1, v2))

# Set the desired distance between the carbon atom and the attached oxygen atom
CH_distance = 1.1  # typical C-H single bond length in angstroms
CO_distance = 1.43  # typical C-O single bond length in angstroms
C_O_distance = 1.2  # typical C=O double bond length in angstroms
OH_distance = 0.97  # typical O-H bond length in angstroms

# Read the graphene structure
graphene = read('graphene_structure/gaussian_opt_cc_pvdz.pdb')

# Remove the edge hydrogen atom
edge_carbon_position, edge_hydrogen_position = remove_edge_hydrogen(graphene, CH_distance)

# Find the direction from the edge carbon to the edge hydrogen
normalized_parallel = ((edge_hydrogen_position - edge_carbon_position) /
                       np.linalg.norm(edge_hydrogen_position - edge_carbon_position))

# Determine the positions for the oxygen atoms
carbonyl_oxygen_position = edge_carbon_position + normalized_parallel * C_O_distance

carbonyl_oxygen_atom = Atoms('O', positions=[carbonyl_oxygen_position])

graphene.extend(carbonyl_oxygen_atom)

for site in select_sites:
    graphene_carbonyl = graphene.copy()

    # get the index of the selected carbon atoms
    i_index = int(site[0])
    round_distance = int(site[3])

    # Determine the positions for the oxygen atoms
    oxygen_position_i = carbon_coords[i_index] + normalized_perpendicular * CO_distance
    hydrogen_position_i = oxygen_position_i + normalized_perpendicular * OH_distance

    # Create and add the oxygen atoms to the structure
    oxygen_atom_i = Atoms('O', positions=[oxygen_position_i])
    hydrogen_atom_i = Atoms('H', positions=[hydrogen_position_i])

    graphene_carbonyl.extend(oxygen_atom_i)
    graphene_carbonyl.extend(hydrogen_atom_i)

    # Write the structure to a gjf file
    filename = 'graphene_structure/graphene_{}.gjf'.format(round_distance)
    graphene_carbonyl.write(filename)
