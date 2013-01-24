

class GibbsTransitionModel(object):
    def __init__(self):
        pass
        
    def transition(self, network, state):
        nodes = network.get_nodes([])
        for node in nodes:
            #reduce this node's cpd
            parents=network.get_parents(node)
            if parents:
                evidence=[(parent,state[parent]) for parent in parents]
                reduced_cpd = node.get_cpd_reduced(evidence)
            else:
                reduced_cpd = node.get_cpd()
                
            
                
            #reduce the children's cpds
            children = network.get_children(node)
            for child in children:
                
                #reduce this node's cpd
                parents=network.get_parents(child)
                if parents:
                    evidence=[(parent,state[parent]) for parent in parents]
                    reduced_child_cpd = child.get_cpd_reduced(evidence)
                else:
                    reduced_child_cpd = child.get_cpd()
                reduced_cpd = reduced_cpd.multiplication(reduced_child_cpd)
                
            
        return state
            
        

class MarkovChainSampler(object):
    def __init__(self):
        pass
        
    def generateMarkovChain(self, network, time_steps, transition_model, initial_state):
        state=initial_state
        for t in range(time_steps):
            yield state
            state=transition_model.transition(network, state)
        
