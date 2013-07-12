import random
import copy

def weighted_random(weights):
    '''
    Implements roulette-wheel-sampling.
    @param weights: A List of float-values.
    @returns: Index of the selected entity
    '''
    counter = random.random() * sum(weights)
    for i,w in enumerate(weights):
        counter -= w
        if counter <=0:
            return i

class GibbsTransitionModel(object):
    '''
    Implements Gibbs-sampling. Can be used to constuct a Markov Chain and is
    mainly used by MarkovChainSampler. This transition model can only be used
    if the product of each variable and the variables in it's  markov blanket 
    can be computed in closed form. This is currently only the case for discrete
    variables / ProbabilityTables, but could possibly extended to the continuous
    setting by assuming gaussian forms for the products or using only classes of
    pdfs for which closed forms are computable.
    
    If the pdf-classes used can not offer this kind of computation you should
    use the MetropolisHastingsTransitionModel, as it only requires to compute
    a single probability, which can way easier be obtained.
    
    Implemented after "Probabilistic Graphical Models, Daphne Koller and Nir Friedman"(p.506)
    '''
    def __init__(self):
        pass
        
    def transition(self, network, state, extern_evidence):
        '''
        Does one single state transition.
        @param network: A BayesNet.
        @param state: The current state of the BayesNet. Given as a Dict from
            RandomNode to Value
        @param extern_evidence: Evidence that is given by the user. This is a
            Dict from Node to Evidence.
        '''
        nodes = network.get_nodes([])
        nodes_to_resample=[n for n in nodes if not n in extern_evidence.keys() or extern_evidence[n].get_unique_value() == None]

        for node in nodes_to_resample:
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
                evidence=[(parent,state[parent]) for parent in parents if parent != node]
                evidence.append((child,state[child]))
                reduced_child_cpd = child.get_cpd_reduced(evidence)

                reduced_cpd = reduced_cpd.multiplication(reduced_child_cpd)
                
            new_state=weighted_random(reduced_cpd.get_table())
            state[node]=node.get_value_range()[new_state]

        return state
        
class MetropolisHastingsTransitionModel(object):
    '''
    Implements the Metropolis-Hastings-Algorithm. Can be used to constuct a Markov Chain.
    
    After "Probabilistic Graphical Models, Daphne Koller and Nir Friedman"(p.644)
    '''
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
        '''
        Does one single state transition.
        @param network: A BayesNet.
        @param state: The current state of the BayesNet. Given as a Dict from
            RandomNode to Value
        @param extern_evidence: Evidence that is given by the user. This is a
            Dict from Node to Evidence.
        '''
        nodes = network.get_nodes([])
        nodes_to_resample=[n for n in nodes if not n in extern_evidence.keys() or extern_evidence[n].get_unique_value() == None]
        for node in nodes_to_resample:
            #propose a new value for this variable:
            current_value = state[node]
            #print node.sample_local(current_value, extern_evidence)
            proposed_value, cdf_ratio = node.sample_local(current_value, extern_evidence)
            
            p_of_proposal_given_mb = self._compute_p_of_value_given_mb(network, state, node, proposed_value)
            p_of_current_given_mb = self._compute_p_of_value_given_mb(network, state, node, current_value)
            #print "acceptance_probability = min(1.0,  "+str(p_of_proposal_given_mb)+" / "+str(p_of_current_given_mb) + " * "+str(cdf_ratio)
            acceptance_probability = min(1.0,  p_of_proposal_given_mb/p_of_current_given_mb * cdf_ratio * 1.0/1.0)
            if random.random() <= acceptance_probability:
                state[node]=proposed_value
            
        return state    
        

class MarkovChainSampler(object):
    '''
    Can be used to generate a Markov Chain by sampling a Bayesian Network. This
    object is mainly used by the MCMC inference class.
    '''
    def __init__(self, transition_model, convergence_test):
        '''
        @param transition_model: This object is used to determine the next state
            for the chain. Can be GibbsTransitionModel or MetropolisHastingsTransitionModel.
        @param convergence_test: A Test that is being used to determine if the
            markov chain has converged to its stationary distribution. For example
            ConvergenceTestSimpleCounting.
        '''
        self.transition_model=transition_model
        self.convergence_test=convergence_test
        
    def set_convergence_test(self, test):
        self.convergence_test=test
        
    def generateMarkovChain(self, network, time_steps, initial_state, evidence={}, variables_of_interest=[]):
        '''
        This function generates a markov chain by sampling from a bayesian network.
        It is possible to use different transition functions.
        
        After "Probabilistic Graphical Models, Daphne Koller and Nir Friedman"(p.509)
        
        @param network: A BayesNet.
        @param time_steps: Integer specifying how long the chain shall be.
        @param initial_state: The state from which transition will start.
        @param evidence: A Dict from RandomNode to Evidence.
        @param variables_of_interest: If not all variable instantiations are needed
            this List of RandomNode objects can be used to select which Nodes
            are mentioned in the return object.
        
        @returns: A Generator-object for a List of States. Each state is a Dict
            from RandomNode to Value
        '''
        self.convergence_test.reset()
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
            state=self.transition_model.transition(network, state, evidence)
        #finally sample from the target distribution
        for t in xrange(time_steps):
            
            if variables_of_interest:
                yield self._reduce_state_to_variables_of_interest(state, variables_of_interest)
            else:
                yield state
            state=self.transition_model.transition(network, state, evidence)
            
    def _reduce_state_to_variables_of_interest(self, state, variables_of_interest):
        return dict((k,v) for (k,v) in state.iteritems() if k in variables_of_interest)
        
