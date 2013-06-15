from  primo.reasoning import MarkovChainSampler
from primo.reasoning import GibbsTransitionModel
from primo.reasoning import MetropolisHastingsTransitionModel
from primo.reasoning.density import ProbabilityTable
class MCMC(object):
    def __init__(self, bn):
    
        #self.transition_model = GibbsTransitionModel()
        self.transition_model = MetropolisHastingsTransitionModel()
        self.bn=bn
        self.mcs = MarkovChainSampler()
        self.times=5000

    def calculate_marginal(self):
        pass
    def calculate_PriorMarginal(self,variables,AssumedDensity):
        return self.calculate_PosteriorMarginal(variables,dict(),AssumedDensity)


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
            for node,value in evidence.items():
                
                if state[node] != value:
                    compatible = False
                    break
            
            if compatible:
                compatible_count = compatible_count + 1
            
            number_of_samples = number_of_samples + 1

        probability_of_evidence = float(compatible_count)/float(number_of_samples)
        return probability_of_evidence
        
    def _generateInitialStateWithEvidence(self, evidence):
        state=[]
        for var in self.bn.get_nodes([]):
            if var in evidence.keys():
                state.append((var,evidence[var]))
            else:
                state.append((var,var.sample_proposal()))
        return dict(state)

