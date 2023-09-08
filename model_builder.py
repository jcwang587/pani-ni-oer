from ase.io import read
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Read the graphene structure
graphene = read('graphene_structure/Graphene.pdb')

# Extract the coordinates of carbon atoms
carbon_coords = [atom.position for atom in graphene if atom.symbol == 'C']

# Calculate the Euclidean distances between all carbon pairs
distances = pdist(carbon_coords)
square_distances = squareform(distances)

# Round the distances to 2 decimal places
square_distances = np.round(square_distances, 0)

print(square_distances)
