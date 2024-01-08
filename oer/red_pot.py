import numpy as np


def electrochem_potential(reactant, product):
    return (product - reactant) * ev2kjmol * kjmol2v - 0.0591 * 14


# Free energy
g1_ni4oh3 = -930.63454
g2_ni4oh3_oh = -940.287597
g3_ni4oh3_o = -936.856913
g4_ni4oh2_o_o = -931.842832
g5_ni4oh3_o2 = -940.490872
g91_oh = -11.69119177
g92_h2o = -14.317398
g93_o2 = -9.89704748

ev2kjmol = 96.485
kjmol2v = 1000 / 96485.33289

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
step4_product = g1_ni4oh3 + g93_o2
step4_potential = electrochem_potential(step4_reactant, step4_product)

step4p_reactant = g4_ni4oh2_o_o + g91_oh + g91_oh
step4p_product = g2_ni4oh3_oh + g93_o2
step4p_potential = electrochem_potential(step4p_reactant, step4p_product)

print("redox potential of step 1:", step1_potential, "V")
print("redox potential of step 2:", step2_potential, "V")
print("redox potential of step 3:", step3_potential, "V")
print("redox potential of step 4:", step4_potential, "V")
print("redox potential of step 4p:", step4p_potential, "V")
