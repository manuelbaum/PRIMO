# -*- coding: utf-8 -*-

import copy
import math
import random

import numpy
from scipy.stats

from primo.nodes

class Density(object):
    '''TODO: write doc'''

    def __init__(self):
        super(Density, self).__init__()
        
    def add_variables(self, variables):
        for v in variables:
            self.add_variable(v)


class BetaParameters(object):
    '''
    This represents the parameters for the beta-density class.
    '''
    def __init__(self, p0, p, q0, q):
        #vector of coefficients for parent values to compute p
        self.p=p
        #vector of coefficients for parent values to compute q
        self.q=q
        #bias for p
        self.p0=p0
        #bias for q
        self.q0=q0


class ExponentialParameters(object):
    '''
    This represents the parameters for the Exponential-density class.
    '''
    def __init__(self, b0, b):
        #lambda a-priori
        self.b0=b0
        #a dict (node,coefficient) that holds the weights that define the depency on each node
        self.b=b


class GaussParameters(object):
    '''
    This represents the parameters for the Gauss-density class.
    '''
    def __init__(self, b0,b,var):
        #offset for the mean of this variable, a priori
        self.b0=b0
        #a vector that holds one weight for each variable that this density depends on
        self.b=b
        #the variance
        self.var=var
        

class NDGaussParameters(object):
    def __init__(self, mu, cov):
        self.mu=mu
        self.cov=cov



class Beta(Density):
    '''
    This class represents an beta probabilty density. Unfortunately this
    is currently a little bulky to use as the parameters for the dependency are
    not very transparent. This is how the dependency works:
    
    The parameters p,q for the exponential distribution are computed analogous
    as the activation of a perceptron with sigmoid-activation function:
    output_scale * sigmoid(input_scale* (b0 + b'state)) where b'state means the dot product between b (a vector
    of weights) and state (a vector with a value for each variable that this
    density depends on). Here: sigmoid=1/(1+exp(-x))
    The parameters output_scale and input_scale can be used to strech or compress
    the sigmoid.
    
    The reason for this is that the parameters are required to be >0. And with
    linear dependencies on the parents this could in no way be guaranteed.
    
    Why the sigmoid function:
    I had to guarantee that the parameters are > 0. As i did not want to
    impose any restrictions on the value range of the parents it was necessary
    to map the support of the parents values to a valid support for the parameters. In
    other (and maybe more correct words): The dependency function to compute
    p and q needed to be of the form R^n->]0,inf].
    
    The first function that came to my mind was:
    weighted sum of the parents values put into an exponential function. This
    caused problems due to the fast growth of the exponential.
    For that reason i switched to the sigmoid function that guarantees 0<p,q<1.
    And because p,q<1 is not very practical output_scale has been introduced
    to scale from ]0,1[ to ]0,output_scale[. 
    
    input_scale can be used to strech the sigmoid in input_direction.
    '''
    def __init__(self, node):
        self.p0=1
        self.q0=1
        self.p={}
        self.q={}
        self.node=node
        
        self.input_scale=0.1
        self.output_scale=5.0
        
    def set_parameters(self,parameters):
        self.p0=parameters.p0
        self.q0=parameters.q0
        self.p=parameters.p
        self.q=parameters.q
        
    def add_variable(self, variable):
        if( not isinstance(variable,ContinuousNode.ContinuousNode)):
            raise Exception("Tried to add Variable as parent, but is not a ContinuousNode")
        self.p[variable]=0.0
        self.q[variable]=0.0
        
        
    def get_probability(self,value, node_value_pairs):
        p=self._compute_p_given_parents(dict(node_value_pairs))
        q=self._compute_q_given_parents(dict(node_value_pairs))
        probability = scipy.stats.beta(p, q).pdf(value)

        return probability
        
    def _compute_p_given_parents(self, state):
        x = self.p0
        for node in self.p.keys():
            if node in state.keys():
                x = x + self.p[node]*state[node]
        return self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))
        
    def _compute_q_given_parents(self, state):
        x = self.q0
        for node in self.q.keys():
            if node in state.keys():
                x = x + self.q[node]*state[node]
        return self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))


    def sample_global(self, state, lower_limit, upper_limit):
        '''This method can be used to sample from this distribution. It is necessary that 
        a value for each parent is specified and it is possible to constrain the
        value that is being sampled to some intervall.
        @param state: A dict (node->value) that specifies a value for each variable
            that this density depends on.
        @param lower_limit: The lower limit of the interval that is allowed to be
            sampled as value.
        @param upper_limit: The upper limit of the interval that is allowed to be
            sampled as value.
        @returns: The sampled value. A real number.
        '''
        p=self._compute_p_given_parents(state)
        q=self._compute_q_given_parents(state)

        distribution=scipy.stats.beta(p,q)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        return sample      

class Exponential(Density):
    '''
    This class represents an exponential probabilty density. Unfortunately this
    is currently a little bulky to use as the parameters for the dependency are
    not very transparent. This is how the dependency works:
    
    The parameter lambda for the exponential distribution is computed analogous
    as the activation of a perceptron with sigmoid-activation function:
    output_scale * sigmoid(input_scale* (b0 + b'state)) where b'state means the dot product between b (a vector
    of weights) and state (a vector with a value for each variable that this
    density depends on). Here: sigmoid=1/(1+exp(-x))
    The parameters output_scale and input_scale can be used to strech or compress
    the sigmoid.
    
    The reason for this is that the parameter lambda is required to be >0. And with
    linear dependencies on the parents this could in no way be guaranteed.
    
    Why the sigmoid function:
    I had to guarantee that the parameter lambda is > 0. As i did not want to
    impose any restrictions on the value range of the parents it was necessary
    to map the support of the parents values to a valid support for lambda. In
    other (and maybe more correct words): The dependency function to compute
    lambda needed to be of the form R^n->]0,inf].
    
    The first function that came to my mind was:
    weighted sum of the parents values put into an exponential function. This
    caused problems due to the fast growth of the exponential.
    For that reason i switched to the sigmoid function that guarantees 0<lambda<1.
    And because lambda<1 is not very practical output_scale has been introduced
    to scale from ]0,1[ to ]0,output_scale[. 
    
    input_scale can be used to strech the sigmoid in input_direction.
    '''
    def __init__(self, node):
        #the coefficients for the weighted sum of parent-values
        self.b={}
        #bias
        self.b0=0
        #the node that this density is associated with
        self.node=node
        #scaling coefficient to stretch or compress the sigmoid in input-direction
        self.input_scale=1.0
        #scaling coefficient to stretch or compress the sigmoid in output-direction
        self.output_scale=4.0
        
    def set_parameters(self,parameters):
        self.b=parameters.b
        self.b0=parameters.b0
        
    def add_variable(self, variable):
        '''This method needs some serious reworking: Variables should not be denied
        to be parents because of their value range. Instead it should be evaluated
        if they can yield parameters for this distribution that are permitted. This 
        can in any case happen under bad influence coefficients'''
        if( not isinstance(variable,ContinuousNode.ContinuousNode)):
            raise Exception("Tried to add Variable as parent, but is not a ContinuousNode")
        self.b[variable]=0.0
        
    def get_probability(self,value, node_value_pairs):
        
        #Compute the offset for the density and displace the value accordingly
        _lambda = self._compute_lambda_given_parents(dict(node_value_pairs))
        #Evaluate the displaced density at value
        return _lambda*math.exp(-_lambda*value)

    def _compute_lambda_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        _lambda=self.output_scale*1.0/(1.0+math.exp(-x*self.input_scale))
        return _lambda

    def sample_global(self,state, lower_limit, upper_limit):
        '''This method can be used to sample from this distribution. It is necessary that 
        a value for each parent is specified and it is possible to constrain the
        value that is being sampled to some intervall.
        @param state: A dict (node->value) that specifies a value for each variable
            that this density depends on.
        @param lower_limit: The lower limit of the interval that is allowed to be
            sampled as value.
        @param upper_limit: The upper limit of the interval that is allowed to be
            sampled as value.
        @returns: The sampled value. A real number.
        '''
        _lambda=self._compute_lambda_given_parents(state)
        distribution=scipy.stats.expon(loc=0,scale=1.0/_lambda)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
        
        #sample=random.expovariate(_lambda)
        #print "EXPO-SAMPLE: "+str(sample)+" at lambda: "+str(_lambda)
        return sample



class ProbabilityTable(Density):
    '''TODO: write doc'''

    @staticmethod
    def get_neutral_multiplication_PT():
        pt = ProbabilityTable()
        pt.set_probability_table(numpy.array(1.0),[])
        
        return pt


    def __init__(self):
        super(ProbabilityTable, self).__init__()
        self.variables = []

        #need to be 0.0 instead of 0 because of precision
        #otherwise the function set probability doesn't work correctly
        self.table = numpy.array(0.0)

    def get_table(self):
        return self.table

    def get_variables(self):
        return self.variables

    def add_variable(self, variable):
        self.variables.append(variable)

        ax = self.table.ndim
        self.table=numpy.expand_dims(self.table,ax)
        self.table=numpy.repeat(self.table,len(variable.value_range),axis = ax)
        


    def set_probability_table(self, table, nodes):
        if not set(nodes) == set(self.variables):
            raise Exception("The list which should define the ordering of the variables does not match"
                " the variables that this cpt depends on (plus the node itself)")
        if not self.table.ndim == table.ndim:
            raise Exception("The provided probability table does not have the right number of dimensions")
        for d,node in enumerate(nodes):
            if len(node.value_range) != table.shape[d]:
                raise Exception("The size of the provided probability table does not match the number of possible values of the node "+node.name+" in dimension "+str(d))

        self.table = table
        self.variables = nodes

    def parametrize_from_states(self, samples, number_of_samples):
        '''This method uses a list of variable-instantiations to change this nodes internal
            table to represent a joint probability table constructed from the given samples.
            The Argument samples is a list of pairs (RandomNode, value).'''

        self.table = numpy.zeros(self.table.shape)
        for state in samples:
            index = self.get_cpt_index(state.items())
            self.table[index] = self.table[index] + 1

        return self.normalize_as_jpt()
        
    def get_most_probable_instantiation(self):
        '''
        This method returns a list of (node,value)-pairs for which this density
        is at its maximum. Probably more useful if this represents a jpt than when
        it represents a cpt.
        '''
        simple_index=numpy.argmax(self.table)
        tuple_index=numpy.unravel_index(simple_index, self.table.shape)
        return self.get_node_value_pairs(tuple_index)

    def set_probability(self, value, node_value_pairs):
        index = self.get_cpt_index(node_value_pairs)
        self.table[index]=value
        
    def get_probability(self, node_value_pairs):
        index = self.get_cpt_index(node_value_pairs)
        return self.table[index]
        
    def sample_global(self, global_state, variable, allowed_values):
        '''
        This method can be used to sample from the density according to a global
        state containing values for all other variables that this node belongs to.
        @param global_state: A Dict (node -> value) that must hold a value for
            all variables that this density depends on. Except for the variable 
            that it is directly associated with.
        @param variable: The variable that this density is directly associated
            with.
        @param allowed_values: A list of values that are allowed to be sampled.
            This is necessary because external evidence may restrict the value
            range.
        @returns: The sampled value.
        '''
        node_value_pairs=[(node,global_state[node]) for node in self.variables if node != variable]
        probabilities=[self.get_probability(node_value_pairs+[(variable,value)]) for value in allowed_values]
        idx=weighted_random(probabilities)
        return allowed_values[idx]

    def get_cpt_index(self, node_value_pairs):
        '''
        Can be used to determine the index in this densitys cpt that accords to
        a completely specified node-value combination for all nodes that this
        density depends on
        @param node_value_pairs: A list of (Node,Value) pairs
        @returns: A tuple representing the index
        '''
        nodes, values = zip(*node_value_pairs)
        index = []
        for node in self.variables:
            index_in_values_list = nodes.index(node)
            value = values[index_in_values_list]
            index.append(node.value_range.index(value))
        return tuple(index)
        
    def get_node_value_pairs(self, index):
        '''
        Can be used to determine the node-value combination that belongs to some
        index for the contitional probabilty table. That state needs to be fully
        specified/all variables this density depends on need to be specified.
        
        This method should probably only be used internally.
        
        @param index: A tuple 
        @returns: a list of (node,value) pairs
        '''
        nv_pairs=[]
        for index_of_value,var in zip(index,self.variables):
            nv_pairs.append((var,var.value_range[index_of_value]))
        return nv_pairs


    def is_normalized_as_cpt(self,owner):
        '''
        This method can be used to determine if this density is a valid cpt for
        some variable. This important as this class can equally represent jpts.
        @param owner: The variable for which normalization-constraints should be
            valid.
        @returns: boolean
        '''

        dim_of_owner = self.variables.index(owner)
        sum_of_owner_probs = numpy.sum(self.table, dim_of_owner)

        return set(sum_of_owner_probs.flatten()) == set([1])

    def is_normalized_as_jpt(self):
        '''
        This method can be used to determine if this density is a valid jpt for
        some variable. This important as this class can equally represent cpts.
        @returns: boolean
        '''
        '''Returns whether the cpd is summed to one'''
        return numpy.sum(self.table) == 1.0

    def normalize_as_jpt(self):
        '''This method normalizes this ProbabilityTable so it represents a valid joint probability table'''
        #self.table = self.table * 1.0 / numpy.sum(self.table)
        #new instance for returning
        retInstance = ProbabilityTable()
        retInstance.table = copy.copy(self.table)
        retInstance.table = retInstance.table * 1.0 / numpy.sum(retInstance.table)
        retInstance.variables = copy.copy(self.variables)
        return retInstance
        
        #this is the old code:
        #return self.table * 1.0 / numpy.sum(self.table)

    def multiplication(self, inputFactor):
        '''This method returns a unified ProbabilityTable which contains the variables of both; the inputFactor
            and this factor(self). The new values of the returned factor is the product of the values from the input factors
            which are compatible to the variable instantiation of the returned value.'''
        #init a new probability tabel
        factor1 = ProbabilityTable()

        #all variables from both factors are needed
        factor1.variables = copy.copy(self.variables)

        for v in (inputFactor.variables):
            if not v in factor1.variables:
                factor1.variables.append(v)

            #the table from the first factor is copied
            factor1.table = copy.copy(self.table)

        #and extended by the dimensions for the left variables
        for curIdx in range(factor1.table.ndim, len(factor1.variables)):
            ax = factor1.table.ndim
            factor1.table=numpy.expand_dims(factor1.table,ax)
            factor1.table=numpy.repeat(factor1.table,len(factor1.variables[curIdx].value_range),axis = ax)

        #copy factor 2 and it's variables ...
        factor2 = ProbabilityTable()
        factor2.variables = copy.copy(inputFactor.variables)
        factor2.table = copy.copy(inputFactor.table)

        #extend the dimensions of factors 2 to the dimensions of factor 1
        for v in factor1.variables:
            if not v in factor2.variables:
                factor2.variables.append(v)

        for curIdx in range(factor2.table.ndim, len(factor2.variables)):
            ax = factor2.table.ndim
            factor2.table=numpy.expand_dims(factor2.table,ax)
            factor2.table=numpy.repeat(factor2.table,len(factor2.variables[curIdx].value_range),axis = ax)

        #sort the variables to the same order
        for endDim,variable in enumerate(factor1.variables):
            startDim = factor2.variables.index(variable);
            if not startDim == endDim:
                factor2.table = numpy.rollaxis(factor2.table, startDim, endDim)
                factor2.variables.insert(endDim,factor2.variables.pop(startDim))

        #pointwise multiplication
        if factor1.table.shape != factor2.table.shape:
            raise Exception("Multiplication: The probability tables have the wrong dimensions for unification!")

        factor1.table = factor1.table *factor2.table;

        return factor1


    def marginalization(self, variable):
        '''This method returns a new instantiation with the given variable summed out.'''

        if not variable in self.variables:
            raise Exception("Marginalization: The given variable isn't in the ProbabilityTable!")

        #new instance for returning
        retInstance = ProbabilityTable()
        retInstance.table = copy.copy(self.table)
        retInstance.variables = copy.copy(self.variables)

        ax = retInstance.variables.index(variable)

        retInstance.table = numpy.sum(retInstance.table,ax)
        retInstance.variables.remove(variable)

        return retInstance


    def reduction(self, evidence):
        '''Returns a reduced version of this ProbabilityTable, evidence is a list of pairs.
            Important: This node is not being changed!'''
        reduced = ProbabilityTable()
        reduced.variables = copy.copy(self.variables)
        reduced.table = self.table
        for node,value in evidence:

            axis=reduced.variables.index(node)
            position=node.value_range.index(value)
            reduced.table = numpy.take(reduced.table,[position],axis=axis)

            reduced.table=reduced.table.squeeze()
            reduced.variables.remove(node)

        return reduced

    def set_evidence(self,evidence):
        '''Returns a new version of the ProbabilityTable with only the evidence
        not equal zero'''

        ev = ProbabilityTable()
        ev.variables = copy.copy(self.variables)
        ev.table = numpy.zeros(self.table.shape)
        tmpCpd = self.table

        pos_variable = ev.variables.index(evidence[0])
        pos_value = ev.variables[pos_variable].value_range.index(evidence[1])

        ev.table = numpy.rollaxis(ev.table,pos_variable,0)
        tmpCpd = numpy.rollaxis(tmpCpd,pos_variable,0)
        ev.variables.insert(0,ev.variables.pop(pos_variable))

        ev.table[pos_value] = tmpCpd[pos_value]

        return ev
        
    def copy(self):
        '''Returns a copied version of this probabilityTable'''
        
        ev = ProbabilityTable()
        ev.variables = copy.copy(self.variables)
        ev.table = copy.copy(self.table)
        
        return ev



    def division(self, factor):
        '''Returns a new ProbabilityTable which is the result of dividing this one by the one given
            with the argument factor'''
        divided = ProbabilityTable()
        variables = list(set(self.variables) | set(factor.variables))
        for variable in variables:
            divided.add_variable(variable)
        for variable in variables:
            for value in variable.get_value_range():
                index = "lol"
        raise Exception("Sorry, called unimplemented method ProbabilityTable.division()")


    def __str__(self):
        return str(self.table)


class Gauss(Density):
    '''
    This class represents a one-dimensional normal distribution with a mean that
    depends linear on the parents but with invariant variance.'''

    def __init__(self,variable):
        super(Gauss, self).__init__()
        
        self.b0=0#numpy.array([0.0])
        self.b={}
        self.var=1.0
        
    def set_parameters(self,parameters):
        self.set_b0(parameters.b0)
        self.set_b(parameters.b)
        self.set_var(parameters.var)
        
    def add_variable(self, variable):

        if not isinstance(variable, primo.nodes.ContinuousNode):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable is not continuous")
        self.b[variable]=0.0
    

    def get_probability(self, x, node_value_pairs):
        
        reduced_mu = self.b0
        for node,value in node_value_pairs:
            reduced_mu = reduced_mu + self.b[node]*value
        return scipy.stats.norm(reduced_mu, numpy.sqrt(self.var)).pdf(x)
        
        
    def set_b(self, variable, b):
        if not variable in b.keys():
            raise Exception("Tried to set dependency-variable b for a variable that has not yet been added to this variable's dependencies")
        self.b[variable]=b
        
    def set_b(self, b):
        if not set(self.b.keys())==set(b.keys()):
            raise Exception("The variables given in the new b do not match the old dependencies of this density")
        self.b=b
        
    def set_b0(self, b0):
        self.b0=b0
        
    def set_var(self, var):
        self.var=var
        
    def _compute_offset_given_parents(self, state):
        x = self.b0
        for node in self.b.keys():
            if node in state.keys():
                x = x + self.b[node]*state[node]
        return x
        
    def sample_global(self,state,lower_limit,upper_limit):
        '''This method can be used to sample from this distribution. It is necessary that 
        a value for each parent is specified and it is possible to constrain the
        value that is being sampled to some intervall.
        @param state: A dict (node->value) that specifies a value for each variable
            that this density depends on.
        @param lower_limit: The lower limit of the interval that is allowed to be
            sampled as value.
        @param upper_limit: The upper limit of the interval that is allowed to be
            sampled as value.
        @returns: The sampled value. A real number.
        '''
        
        distribution=scipy.stats.norm(self._compute_offset_given_parents(state), self.var**0.5)
        
        lower_cdf=distribution.cdf(lower_limit)
        upper_cdf=distribution.cdf(upper_limit)
        
        sample_in_integral=random.uniform(lower_cdf, upper_cdf)
        
        sample=distribution.ppf(sample_in_integral)
    
    
        return sample



class NDGauss(Density):
    '''
    This class represents an N-Dimensional gaussian density. It is currently not
    tested for inclusion into a bayesian network, but it is used to compute return
    values for inference in the continuous setting. This is not optimal yet,
    as for example, when computing the map hypothesis of a density with two or
    more modes the mean of the gaussian could be in an area of state space with
    very low probability. It would be sensible to also introduce a density
    mixture of gaussian (or similar), to account for such problems. That density
    could for example be learned with EM.
    '''

    def __init__(self):
        super(NDGauss, self).__init__()
        
        self.mu=numpy.array([0.0])
        self.C=numpy.array([[1.0]])
        self.variables=[]

        
    def add_variable(self, variable):
        v_min,v_max=variable.get_value_range()
        if not  (v_min>= -float("Inf") and v_max <=float("Inf")):
            raise Exception("Tried to add Variable into Gaussian densitiy, but variable had wrong value-range")
        self.variables.append(variable)
        
        
        m=len(self.variables)
        self.mu.resize([m,1])
        self.C.resize((m,m))
        
        self.C[m-1,m-1]=1.0
        
    def set_parameters(self,parameters):
        self.set_mu(parameters.mu)
        self.set_cov(parameters.cov)
        
    def set_mu(self, mu):
        self.mu=mu
        
    def set_cov(self, C):
        self.C=C
        
    def sample(self):
        return numpy.random.multivariate_normal(self.mu,self.C)
            
            
    def parametrize_from_states(self, samples, number_of_samples):
        '''This method uses a list of variable-instantiations to change this node's parametrization
         to represent a Gaussian constructed from the given samples.
            The Argument samples is a list of pairs (RandomNode, value).'''
            
        X=numpy.empty((number_of_samples, len(self.variables)))
        for i,state in enumerate(samples):
            for j,variable in enumerate(self.variables):
                X[i,j]=state[variable]

        self.mu=numpy.mean(X,axis=0)
        self.C=numpy.cov(X.transpose())
        return self
        
    def get_most_probable_instantiation(self):
        return self.mu
        
    def __str__(self):
        ret= "Gauss(\nmu="+str(self.mu)+"\nC="+str(self.C)+")"
        return ret
