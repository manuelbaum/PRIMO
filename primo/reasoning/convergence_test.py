class ConvergenceTestSimpleCounting(object):
    def __init__(self, limit):
        self.chain_length=0
        self.limit=limit
    def has_converged(self, state):
        self.chain_length= self.chain_length +1
        return self.chain_length >= self.limit
    def reset(self):
        self.chain_length=0
