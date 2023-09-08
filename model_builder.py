from ase.io import read
import numpy as np
from scipy.spatial.distance import pdist, squareform

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

# Randomly select the distance_values from the fourth column of distance_array
random_distances = np.random.choice(distance_values, replace=False)