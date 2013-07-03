from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
from primo.reasoning import MetropolisHastingsTransitionModel
from primo.reasoning.density import ProbabilityTable

class ConvergenceTestSimpleCounting(object):
    def __init__(self, limit):
        self.chain_length=0
        self.limit=limit
    def has_converged(self, state):
        self.chain_length= self.chain_length +1
        return self.chain_length >= self.limit

class MCMC(object):
    def __init__(self, bn):
    
        #self.transition_model = GibbsTransitionModel()
        self.transition_model = MetropolisHastingsTransitionModel()
        self.bn=bn
        
        self.times=1000
        self.number_of_chains=4

        self.mcs = MarkovChainSampler()
        self.mcs.set_convergence_test(ConvergenceTestSimpleCounting(100))

    def calculate_marginal(self):
        pass
    def calculate_PriorMarginal(self,variables,AssumedDensity):
        return self.calculate_PosteriorMarginal(variables,dict(),AssumedDensity)

    def calculate_MAP(self, variables_of_interest, evidence, AssumedDensity):
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, self.transition_model, initial_state, evidence, variables_of_interest)
        
        density = AssumedDensity()
        density.add_variables(variables_of_interest)
        density = density.parametrize_from_states(chain,self.times)
        return density.get_most_probable_instantiation()


    def calculate_PosteriorMarginal(self,variables_of_interest,evidence,AssumedDensity):
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, self.transition_model, initial_state, evidence, variables_of_interest)
        
        density = AssumedDensity()
        density.add_variables(variables_of_interest)
        density = density.parametrize_from_states(chain,self.times)
        return density
        
    
    
    
    def calculate_PoE(self,evidence):
    
        initial_state=self._generateInitialStateWithEvidence(evidence)
        chain = self.mcs.generateMarkovChain(self.bn, self.times, self.transition_model, initial_state)
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

