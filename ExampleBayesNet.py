from  core.BayesNet import *
from  core.Node import *

bn = BayesNet()
n1 = Node("Node1")
n2 = Node("Node2")
n3 = Node("Node3")

bn.add_node(n1)
bn.add_node(n2)

bn.add_edge(n1,n2)

n = bn.get_node("Node1")
print n.name

ns = bn.get_nodes(["Node2","Node1"])
for n in ns:
    print n.name

print "Removing existing edge"
bn.remove_edge(n1, n2)
print "Removing not existing edge"
bn.remove_edge(n1, n2)


bn.draw()
