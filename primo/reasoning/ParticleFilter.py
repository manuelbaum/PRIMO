# -*- coding: utf-8 -*-
import primo.reasoning.GibbsTransitionModel as gtm

def particle_filtering(e, N, dbn):
    S = dbn.sample_from_prior_distribution(N)
    W = [(1. / N)] * N
    
    print S
    
    for i in xrange(0, N):
        print S[i]
        S[i] = gtm.transition(dbn, S[i])
    
    print " --------------------------------------------------------------- "
    print S
#    for i in xrange(1, self.iterations):
#        self.particles = gtm.transition(dbn, state)