


class Evidence(object):
    '''
    A generic class for evidence. Can not be used on its own. Look for its
    subclasses.
    '''    
    def __init__(self):
        pass
        
    def is_compatible(self, value):
        '''
        This method can be used to check if a value is consistent with some
        evidence.        
        '''
        raise Exception("Not defined for this kind of Evidence")
        
    def get_unambigous_value(self):
        '''
        Sometimes only one value of some domain is compatible with the evidence.
        This is obviously the case for EvidenceEqual. It is then possible to
        use this value to speed up computations.
        
        @return: The only value compatible with the evidence or else None.
        '''
        return None
        
class EvidenceEqual(Evidence):
    '''
    This class can be used to specify evidence that a variable has taken some 
    specified value.
    e.g. a=5
    '''
    def __init__(self, value):
        self.value=value
        
    def is_compatible(self, value):
        return self.value==value
        
    def get_unambigous_value(self):
        return self.value
        
class EvidenceIntervall(Evidence):
    '''
    This class can be used to specify evidence that a variable has taken on
    some value in a defined interval.
    e.g. 2<=a<=5
    '''
    def __init__(self,min_val,max_val):
        self.min_val=min_val
        self.max_val=max_val
        
    def is_compatible(self, value):
        return self.min_val <= value and value<=self.max_val
        

class EvidenceLower(Evidence):
    '''
    This class can be used to specify evidence that a variable has taken on
    some value lower than some threshold.
    e.g. a<3
    '''
    def __init__(self,limit):
        self.limit=limit
        
    def is_compatible(self, value):
        return value<self.limit
        
class EvidenceHigher(Evidence):
    '''
    This class can be used to specify evidence that a variable has taken on
    some value higher than some threshold.
    e.g. a>3
    '''
    def __init__(self,limit):
        self.limit=limit
        
    def is_compatible(self, value):
        return value>self.limit
