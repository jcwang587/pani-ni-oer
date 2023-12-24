import numpy as np


def electrochem_potential(reactant, product):
    return (product - reactant) * ev2kjmol * kjmol2v - rhe


def chemical_energy(reactant, product):
    return (product - reactant) * ha2kjmol


e1_ni4oh3 = -930.43487
e2_ni4oh3_oh = -940.47034
e3_ni4oh3_o = -936.83637
e4_ni4oh2_o_o = -931.65616
e5_ni4oh3_o2 = -940.14993
e91_oh = -7.0803312
e92_h2o = -14.220392
e93_o2 = -8.7344601

c1_ni4oh3 = 15.364773
c2_ni4oh3_oh = 15.684409
c3_ni4oh3_o = 15.401384
c4_ni4oh2_o_o = 15.202361
c5_ni4oh3_o2 = 15.461829
c91_oh = -0.238268
c92_h2o = 0.084860
c93_o2 = -0.420961

ev2kjmol = 96.485
ha2kjmol = 2625.4996
kjmol2v = 1000 / 96485.33289
rhe = 3.43

g1_ni4oh3 = e1_ni4oh3 + c1_ni4oh3
g2_ni4oh3_oh = e2_ni4oh3_oh + c2_ni4oh3_oh
g3_ni4oh3_o = e3_ni4oh3_o + c3_ni4oh3_o
g4_ni4oh2_o_o = e4_ni4oh2_o_o + c4_ni4oh2_o_o
g5_ni4oh3_o2 = e5_ni4oh3_o2 + c5_ni4oh3_o2

step1_reactant = g1_ni4oh3
step1_product = g2_ni4oh3_oh
step1_potential = electrochem_potential(step1_reactant, step1_product)
