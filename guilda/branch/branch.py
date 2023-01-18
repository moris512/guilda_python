import numpy as np
from numpy import exp


class Branch(object):
    '''
    Branch base class
    '''
    
    def __init__(self, from_: int, to: int) -> None:
        """
        _summary_

        Args:
            from_ (int): _description_
            to (int): _description_
        """        
        self.from_ = int(from_)
        self.to = int(to)


