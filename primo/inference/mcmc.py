import copy
import random

from primo.util import weighted_random


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
            state[var]=var.sample_global(state, evidence)
        return state

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


class ConvergenceTestSimpleCounting(object):
    def __init__(self, limit):
        self.chain_length=0
        self.limit=limit
    def has_converged(self, state):
        self.chain_length= self.chain_length +1
        return self.chain_length >= self.limit
    def reset(self):
        self.chain_length=0
