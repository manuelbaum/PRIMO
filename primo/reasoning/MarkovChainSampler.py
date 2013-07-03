import random
import copy
def weighted_random(weights):
    counter = random.random() * sum(weights)
    for i,w in enumerate(weights):
        counter -= w
        if counter <=0:
            return i

class GibbsTransitionModel(object):
    def __init__(self):
        pass
        
    def transition(self, network, state, extern_evidence):
        nodes = network.get_nodes([])
        nodes_to_resample=[n for n in nodes if not n in extern_evidence.keys() or extern_evidence[n].get_unambigous_value() == None]
        #print nodes_to_resample
        for node in nodes_to_resample:
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
        
class MetropolisHastingsTransitionModel(object):
    def __init__(self):
        pass
        
    def _compute_p_of_value_given_mb(self, network, state, node, value):
        parents=network.get_parents(node)
        if parents:
            evidence=[(parent,state[parent]) for parent in parents]
        else:
            evidence=[]    
        p = node.get_probability(value,evidence)
           
        children = network.get_children(node)
        for child in children:
                
            #reduce this node's cpd
            parents=network.get_parents(child)
            evidence=[(parent,state[parent]) for parent in parents if parent != node]
            evidence.append((node,value))
            p = p * child.get_probability(state[child],evidence)
        return p
        
    def transition(self, network, state, extern_evidence):
        nodes = network.get_nodes([])
        nodes_to_resample=[n for n in nodes if not n in extern_evidence.keys() or extern_evidence[n].get_unambigous_value() == None]
        for node in nodes_to_resample:
            #propose a new value for this variable:
            current_value = state[node]
            proposed_value = node.sample_local(current_value, extern_evidence)
            
            p_of_proposal_given_mb = self._compute_p_of_value_given_mb(network, state, node, proposed_value)
            p_of_current_given_mb = self._compute_p_of_value_given_mb(network, state, node, current_value)
            
            acceptance_probability = min(1.0,  p_of_proposal_given_mb/p_of_current_given_mb * 1.0/1.0)
            if random.random() <= acceptance_probability:
                state[node]=proposed_value
            
            #new_state=weighted_random(reduced_cpd.get_table())
            #state[node]=node.get_value_range()[new_state]
        #print state
        return state    
        

class MarkovChainSampler(object):
    def __init__(self):
        self.convergence_test=None
        pass
        
    def set_convergence_test(self, test):
        self.convergence_test=test
        
    def generateMarkovChain(self, network, time_steps, transition_model, initial_state, evidence={}, variables_of_interest=[]):
        state=initial_state
        
        if evidence:
            for node in evidence.keys():
                if  not evidence[node].is_compatible(state[node]):
                    raise Exception("The evidence given does not fit to the initial_state specified")
#            constant_nodes = evidence.keys()
#        else:
#            constant_nodes=[]
            
        #let the distribution converge to the target distribution
        while not self.convergence_test.has_converged(state):
            #print state
            state=transition_model.transition(network, state, evidence)
        #finally sample from the target distribution
        for t in xrange(time_steps):
            
            if variables_of_interest:
                yield self._reduce_state_to_variables_of_interest(state, variables_of_interest)
            else:
                yield state
            state=transition_model.transition(network, state, evidence)
            
    def _reduce_state_to_variables_of_interest(self, state, variables_of_interest):
        return dict((k,v) for (k,v) in state.iteritems() if k in variables_of_interest)
        
