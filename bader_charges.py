import numpy as np

# Read charges from ACF.dat file
charges = np.genfromtxt('ACF.dat', usecols=(4,), skip_footer=4, skip_header=2)

# Read ZVAL values from POTCAR file
with open("POTCAR") as f:
    lines = f.readlines()
    zvals = [float(line.split()[-4]) for line in lines if "ZVAL" in line]

# Read atom count and species from POSCAR file
with open("POSCAR") as f:
    lines = f.readlines()
    atom_count = [int(x) for x in lines[6].split()]
    species = lines[5].split()

# Create array that corresponds to ZVAL for each species
zval_array = []
for i in range(len(species)):
    zval_array += [zvals[i]] * atom_count[i]

# Subtract ZVAL from charges and output new file
new_charges = charges - zval_array
np.savetxt("corrected_charges.dat", new_charges, fmt='%.6f')
