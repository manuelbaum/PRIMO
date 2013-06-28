


class Evidence(object):
    def __init__(self):
        pass
        
    def is_compatible(self, value):
        raise Exception("Not defined for this kind of Evidence")
        
    def get_unambigous_value(self):
        return None
        
class EvidenceEqual(Evidence):
    def __init__(self, value):
        self.value=value
        
    def is_compatible(self, value):
        return self.value==value
        
    def get_unambigous_value(self):
        return self.value
        
class EvidenceIntervall(Evidence):
    def __init__(self,min_val,max_val):
        self.min_val=min_val
        self.max_val=max_val
        
    def is_compatible(self, value):
        return self.min_val <= value and value<=self.max_val
        

class EvidenceLower(Evidence):
    def __init__(self,limit):
        self.limit=limit
        
    def is_compatible(self, value):
        return value<self.limit
        
class EvidenceHigher(Evidence):
    def __init__(self,limit):
        self.limit=limit
        
    def is_compatible(self, value):
        return value>self.limit
