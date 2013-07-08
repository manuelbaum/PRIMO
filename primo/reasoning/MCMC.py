from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
from primo.reasoning import MetropolisHastingsTransitionModel
from primo.reasoning.density import ProbabilityTable
from primo.reasoning.convergence_test import ConvergenceTestSimpleCounting


class MCMC(object):
    def __init__(self, bn, times, transition_model=None, convergence_test=None):
        '''
        @param bn: The BayesNet that will be used for inference.
        @param times: How many samples shall be generated for each inference.
        @param transition_model: The transition model that shall be used to
            wander around the state space of the BayesNet.
        @param convergence_test: The ConvergenceTest that shall be used to determine
            if the markov chain that is being generated internally has converged
            to its stationary distribution.
        '''
        self.bn=bn
        self.times=times
    
        if transition_model == None:
            transition_model = MetropolisHastingsTransitionModel()

        if convergence_test == None:
            convergence_test = ConvergenceTestSimpleCounting(100)

        self.mcs = MarkovChainSampler(transition_model,convergence_test)

    def calculate_PriorMarginal(self,variables,AssumedDensity):
        '''
        Calculate the marginal over some variables. 
        @param variables_of_interest: A list containing the variables over which
            the prior marginal shall be defined.
        @param AssumedDensity: A class from primo.reasoning.density . This
            parameter is used to define the class of density for the return value.
        @returns: An object of the class AssumedDensity.
        '''   
        return self.calculate_PosteriorMarginal(variables,dict(),AssumedDensity)

    def calculate_MAP(self, variables_of_interest, evidence, AssumedDensity):
        '''
        Calculate the maximum a posteriori hypothesis given some evidence. 
        @param variables_of_interest: A list containing the variables for which
            the map-hypothesis is wanted.
        @param evidence: A Dict from Node to Evidence.
        @param AssumedDensity: A class from primo.reasoning.density . This
            parameter is used to generate a posterior distribution from which it
            is possible to find the value/set of values that are most probable.
            You could pass a Gauss in a continuous setting here, for example.
        @returns: The most probable instatiaion given the evidence in the form:
            List of pairs (Node, Value).
        '''        
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, initial_state, evidence, variables_of_interest)
        
        density = AssumedDensity()
        density.add_variables(variables_of_interest)
        density = density.parametrize_from_states(chain,self.times)
        return density.get_most_probable_instantiation()


    def calculate_PosteriorMarginal(self,variables_of_interest,evidence,AssumedDensity):
        '''
        Calculate some posterior marginal. 
        @param variables_of_interest: A list containing the variables over which
            the posterior marginal shall be defined.
        @param evidence: A Dict from Node to Evidence.
        @param AssumedDensity: A class from primo.reasoning.density . This
            parameter is used to define the class of density for the return value.
        @returns: An object of the class AssumedDensity.
        '''        
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, initial_state, evidence, variables_of_interest)
        
        density = AssumedDensity()
        density.add_variables(variables_of_interest)
        density = density.parametrize_from_states(chain,self.times)
        return density
        
    
    
    
    def calculate_PoE(self,evidence):
        '''
        Calculate Probability of Evidence.
        @param evidence: A Dict from Node to Evidence.
        @returns: Float number representing the wanted probability.
        '''
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, initial_state)
        compatible_count=0
        number_of_samples=0
        for state in chain:
            compatible = True
            for node,node_evidence in evidence.items():
                
                if not node_evidence.is_compatible(state[node]):
                    compatible = False
                    break
            
            if compatible:
                compatible_count = compatible_count + 1
            
            number_of_samples = number_of_samples + 1

        probability_of_evidence = float(compatible_count)/float(number_of_samples)
        return probability_of_evidence
        
    def _generateInitialStateWithEvidence(self, evidence):
        return self.forward_sample(evidence)
        
    def forward_sample(self, evidence):
        '''
        Generate a sample from the distribution defined by the given BayesNet by
        forward sampling.
        
        @param evidence: A Dict from Node to Evidence.
        '''
        state={}
        for var in self.bn.get_nodes_in_topological_sort():
            if var in evidence.keys():
                value=evidence[var].get_unambigous_value()
                if value == None:
                    value=var.sample_global(state)
                state[var]=value
            else:
                state[var]=var.sample_global(state)
        return state

