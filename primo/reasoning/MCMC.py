import random

def weighted_random(weights):
    counter = random.random() * sum(weights)
    for i,w in enumerate(weights):
        counter -= w
        if counter <=0:
            return i

class GibbsTransitionModel(object):
    def __init__(self):
        pass
        
    def transition(self, network, state):
        nodes = network.get_nodes([])
        for node in nodes:
            #print "----------------Iteration------"
            #print node
            #reduce this node's cpd
            parents=network.get_parents(node)
            if parents:
                evidence=[(parent,state[parent]) for parent in parents]
                reduced_cpd = node.get_cpd_reduced(evidence)
            else:
                reduced_cpd = node.get_cpd()
                
            #print "--reduced cpt"
            #print reduced_cpd
                
            #reduce the children's cpds
            children = network.get_children(node)
            for child in children:
                
                #reduce this node's cpd
                parents=network.get_parents(child)
                evidence=[(parent,state[parent]) for parent in parents if parent != node]
                evidence.append((child,state[child]))
                reduced_child_cpd = child.get_cpd_reduced(evidence)

                #print "--reduced child cpt"
                #print reduced_child_cpd
                reduced_cpd = reduced_cpd.multiplication(reduced_child_cpd)
                
            new_state=weighted_random(reduced_cpd.get_table())
            #print state[node]
            #print new_state
            #print node.get_value_range()
            state[node]=node.get_value_range()[new_state]
            #print state[node]
        return state
            
        

class MarkovChainSampler(object):
    def __init__(self):
        pass
        
    def generateMarkovChain(self, network, time_steps, transition_model, initial_state):
        state=initial_state
        for t in range(time_steps):
            yield state
            state=transition_model.transition(network, state)
        
