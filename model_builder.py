from ase.io import read
from ase import Atoms
import numpy as np
from scipy.spatial.distance import pdist, squareform

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
perpendicular_direction = np.cross(v1, v2)
normalized_perpendicular = perpendicular_direction / np.linalg.norm(perpendicular_direction)

# Set the desired distance between the carbon atom and the attached oxygen atom
CO_distance = 1.43  # typical C-O single bond length in angstroms

for site in select_sites:
    # Read the graphene structure
    graphene = read('graphene_structure/gaussian_opt_cc_pvdz.pdb')

    # get the index of the selected carbon atoms
    i_index = int(site[0])
    j_index = int(site[1])
    round_distance = int(site[3])

    # Determine the positions for the oxygen atoms
    oxygen_position_i = carbon_coords[i_index] + normalized_perpendicular * CO_distance
    oxygen_position_j = carbon_coords[j_index] - normalized_perpendicular * CO_distance

    # Create and add the oxygen atoms to the structure
    oxygen_atom_i = Atoms('O', positions=[oxygen_position_i])
    oxygen_atom_j = Atoms('O', positions=[oxygen_position_j])

    graphene.extend(oxygen_atom_i)
    graphene.extend(oxygen_atom_j)

    # Write the structure to a gjf file
    filename = 'graphene_structure/graphene_{}_{}_{}.gjf'.format(round_distance, i_index, j_index)
    graphene.write(filename)

