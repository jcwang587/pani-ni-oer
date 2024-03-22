from matplotlib import pyplot as plt

# Increase the font sizes
plt.rcParams.update({'font.size': 16})

# Data for plotting
U_RHE = [i/100 for i in range(0, 141)]
delta_G = [4.28240591 - 3 * i for i in U_RHE]

# Create the plot
plt.figure(figsize=(8, 6))  # Adjust the size as needed
plt.plot(U_RHE, delta_G, color='blue', linewidth=2)

# Customize the plot to match the style of the uploaded image
plt.xlim(0.01, 1.4)  # Set x-limits, note that log scale cannot start at 0

# Add a grid, set logarithmic scale
plt.grid(which='both', linestyle='--', linewidth=0.5)

# Set axis labels and title
plt.xlabel(r'$U_{RHE} \ (V)$')
plt.ylabel(r'$\Delta G \ (eV)$')


# Show the plot
plt.show()
