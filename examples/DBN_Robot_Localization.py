# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from primo.core import BayesNet
from primo.core import DynamicBayesNet
from primo.core import TwoTBN
from primo.reasoning import DiscreteNode
import primo.reasoning.particlebased.ParticleFilterDBN as pf
import numpy
from primo.utils import XMLBIF

# Construct a DynmaicBayesianNetwork
dbn = DynamicBayesNet()
B0 = BayesNet()
twoTBN = TwoTBN(XMLBIF.read("Robot_Localization.xmlbif"))

# Configure TwoTBN
x0 = twoTBN.get_node("x0")
x = twoTBN.get_node("x")
door = twoTBN.get_node("door")
twoTBN.set_initial_node(x0.name)

# Configure initial distribution
x0_init = DiscreteNode("x0", ["p0", "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"])
B0.add_node(x0_init)
cpt_x0_init = numpy.array([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
x0_init.set_probability_table(cpt_x0_init, [x0_init])

dbn.B0 = B0
dbn.twoTBN = twoTBN

N = 100
T = 3

pos = 0
def get_evidence_function():
    global pos
    evidence = {}
    if pos == 1 or pos == 3 or pos == 7:
        evidence = {door:"True"}
    else:
        evidence = {door:"False"}
    pos = pos + 1
    if pos == 10:
        pos = 0
    return evidence
    
samples = pf.particle_filtering_DBN(dbn, N, T, get_evidence_function)
w_hit = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
w_all = 0.0
for i in samples:
    (state, w) = samples[i]
#    print state
    if state[x] == "p0":
        w_hit[0] += w
    if state[x] == "p1":
        w_hit[1] += w
    if state[x] == "p2":
        w_hit[2] += w
    if state[x] == "p3":
        w_hit[3] += w
    if state[x] == "p4":
        w_hit[4] += w
    if state[x] == "p5":
        w_hit[5] += w
    if state[x] == "p6":
        w_hit[6] += w
    if state[x] == "p7":
        w_hit[7] += w
    if state[x] == "p8":
        w_hit[8] += w
    if state[x] == "p9":
        w_hit[9] += w
    w_all += w
#
print w_all
print w_hit
#
print("P(..) = " + str(w_hit[3] / w_all))