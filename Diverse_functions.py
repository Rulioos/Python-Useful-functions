"""

 The first function determines if an object is iterable or not.
 The second one determines if a variable of type:
    -str
    -int
    -np.ndarray
    -list
    -range
    -None
 is empty ( null ) or not.
"""

import numpy as np


#Check if item is iterable
def isiterable(item):
    """
    Check if item is iterable
    :param item: random object
    :return:boolean
    """
    try:
        iter(item)
        return True
    except TypeError:
        return False
    
#Check if a variable is empty is her type is in the features list
def void(item):
    """
    Determine if an item can be considered as empty
    :param item: item to evaluate
    :return: boolean
    """
    mapping={int:lambda x:x==0,
             list:lambda x:len(x)==0,
             str:lambda x: len(x.replace(" ",""))==0,
             np.ndarray:lambda x:len(list(x))==0,
             range: lambda x: len(x)==0,
             None:True}
    return mapping[type(item)](item)





