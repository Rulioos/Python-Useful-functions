"""
Fonction used to determine if a variable is empty or null.
Features supported are:
  - String 
  - Integer
  - Float
  - np.ndarray
  - list
Features to come:
  - pandas dataframes
  - random objects
  - functions return 
  - files/directory
  
"""

import numpy as np

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
             None:True}

    return mapping[type(item)](item)
 
#test zone
print(void(0))
print(void([]))
print(void(np.array([])))
print(void("       "))
print(void(""))
print(void("rf"))
