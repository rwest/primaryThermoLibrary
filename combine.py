#! python

import os.path
import fileinput

# First we set up a dictionary of enthalpies at 298 K in kcal/mol
H = dict()
# From Fraklin's DFT-QCI thermo
# CO2	      -94.36       50.99        8.87        9.84       10.63       11.26       12.23       12.90       13.82  0.0  0.0  0.0 
# O	       59.64       36.40        4.96        4.96        4.96        4.96        4.96        4.96        4.96  0.0  0.0  0.0 
# which means the best-guess for CO2 + O(3P) is:
H['CO2 + O(3P)'] = 59.64 + -94.36

# calculate the rest via energy differences taken from J Pys Chem A 108(39) p7985
H['s1'] = H['CO2 + O(3P)'] + 45.4 - 48.8 # using "best estimate" for relative energies
H['s2'] = H['s1'] + 47.2 - 47.1          # using  MRCI+Q(16,13)/6-311+G(3df) + ZPE[CASSCF(16,13)/6-311G(d)]
H['t1'] = H['CO2 + O(3P)'] + 47.7 - 24.7 # using  MRCI+Q(16,13)/6-311+G(3df) + ZPE[CASSCF(16,13)/6-311G(d)]
H['t2'] = H['CO2 + O(3P)'] + 47.7 + 15.5 # using  MRCI+Q(16,13)/6-311+G(3df) + ZPE[CASSCF(16,13)/6-311G(d)]
H['s4'] = H['s1'] + 47.2 - 27.1          # using  MRCI+Q(16,13)/6-311+G(3df) + ZPE[CASSCF(16,13)/6-311G(d)]

#  NB. this neglects differences in the integrals of Cp between 0 and 298 K.

instream = fileinput.input()
for line in instream:
    assert fileinput.isfirstline()
    species_name = os.path.splitext(fileinput.filename())[0]
    H_cal_mol, S_cal_mol_K = instream.next().split()
    H_J_mol, S_J_mol_K = instream.next().split()
    Cp_cal_mol_K_list = instream.next().split()
    Cp_cal_mol_K_string = ("%8s"*7)%tuple(Cp_cal_mol_K_list)
    H_kcal_mol = float(H_cal_mol)/1e3
    # Having done all that, replace it with the value from the dictionary
    H_kcal_mol = H[species_name]
    try:
        chemgraph_name = file(species_name+'.chemgraph').readline().strip()
    except IOError:
        chemgraph_name = '//NoChemgraph//'+species_name
    print "%-10s %10s %10s %s    0.0 0.0 0.0"%(chemgraph_name, H_kcal_mol, S_cal_mol_K, Cp_cal_mol_K_string )
    fileinput.nextfile()

