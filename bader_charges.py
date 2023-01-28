import numpy as np

# Read charges from ACF.dat file
charges = np.genfromtxt('ACF.dat', usecols=(4,), skip_footer=4, skip_header=2)

# Read atom types and numbers from POSCAR file
with open('POSCAR') as f:
    lines = f.readlines()
    atom_types = lines[5].split()
    atom_numbers = list(map(int,lines[6].split()))

# Read ZVAL from POTCAR file
with open('POTCAR') as f:
    zvals = {}
    zval_found = False
    for line in f:
        if 'ZVAL' in line:
            zval_found = True
        if zval_found:
            zvals[line.split()[0]] = float(line.split()[-4])
            zval_found = False

# Create an array of ZVAL values for each atom
zval_array = np.zeros(sum(atom_numbers))
start_index = 0
for i, atom in enumerate(atom_types):
    try:
        zval_array[start_index: start_index + atom_numbers[i]] = zvals[atom]
    except KeyError:
        zval_array[start_index: start_index + atom_numbers[i]] = 0
    start_index += atom_numbers[i]

# Subtract ZVAL from charges
corrected_charges = charges - zval_array

# Output new charges to new file
np.savetxt('corrected_charges.dat', corrected_charges)
