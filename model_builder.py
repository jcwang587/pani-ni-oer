from ase.io import read
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Read the graphene structure
graphene = read('graphene.pdb')

# Extract the coordinates of carbon atoms
carbon_coords = [atom.position for atom in graphene if atom.symbol == 'C']

# Calculate the Euclidean distances between all carbon pairs
distances = pdist(carbon_coords)
square_distances = squareform(distances)

# round the distances to 2 decimal places
square_distances = np.round(square_distances, 0)

# Get unique distances
unique_distances = np.unique(square_distances[square_distances > 0])
print(unique_distances)
import random

np.random.seed(0)  # for reproducibility
random_indices = np.random.choice(len(unique_distances), 13, replace=False)
random_distances = unique_distances[random_indices]
print(random_distances)
