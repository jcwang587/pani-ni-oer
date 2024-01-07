import numpy as np


def electrochem_potential(reactant, product):
    return (product - reactant) * ev2kjmol * kjmol2v


# Free energy
g1_ni4oh3 = -930.63454
g2_ni4oh3_oh = -940.296283
g3_ni4oh3_o = -936.858766
g4_ni4oh2_o_o = -931.844656
g5_ni4oh3_o2 = -940.488191
g91_oh = -10.047892
g92_h2o = -14.324212
g93_o2 = -9.93605306

ev2kjmol = 96.485
kjmol2v = 1000 / 96485.33289
rhe = 3.43

step1_reactant = g1_ni4oh3 + g91_oh
step1_product = g2_ni4oh3_oh
step1_potential = electrochem_potential(step1_reactant, step1_product)

step2_reactant = g2_ni4oh3_oh + g91_oh
step2_product = g3_ni4oh3_o + g92_h2o
step2_potential = electrochem_potential(step2_reactant, step2_product)

step3_reactant = g3_ni4oh3_o + g91_oh
step3_product = g4_ni4oh2_o_o + g92_h2o
step3_potential = electrochem_potential(step3_reactant, step3_product)

step4_reactant = g4_ni4oh2_o_o + g91_oh
step4_product = g5_ni4oh3_o2
step4_potential = electrochem_potential(step4_reactant, step4_product)

step5_reactant = g5_ni4oh3_o2
step5_product = g1_ni4oh3 + g93_o2
step5_potential = electrochem_potential(step5_reactant, step5_product)

step5p_reactant = g5_ni4oh3_o2 + g91_oh
step5p_product = g2_ni4oh3_oh + g93_o2
step5p_potential = electrochem_potential(step5p_reactant, step5p_product)

print("redox potential of step 1:", step1_potential, "V")
print("redox potential of step 2:", step2_potential, "V")
print("redox potential of step 3:", step3_potential, "V")
print("redox potential of step 4:", step4_potential, "V")
print("redox potential of step 5:", step5_potential, "V")
print("redox potential of step 5':", step5p_potential, "V")
