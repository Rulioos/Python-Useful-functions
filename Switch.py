"""
Defines a python switch with all security measures around variable type. It's done without use of dictionnary but dictionnaries
maybe better than lists in that kind of problem. 
Two versions are distributed here:
    - One done with lists
    - Another one done with dictionnaries
  
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
    
#switch with lists
def switch(typ,default,cases):
    """
    Supported types are:
        -int
        -str
     Features only equality case for now.
     
    :param type: The type of value who will be tested in the switch ( int, str, float ,bin ,list )
    :param default: The default action to take if other conditions are not done
    :param cases: value=action
    :return: A switch method to call
    """
    def make_condition(cle):
        return lambda x: x==cle
    
    def check_type(kind,value):
        """Check a value type"""
        if type(value) is kind: return True
        else: return False
    
    #checking typ is a callable type
    if not callable(typ):return "{} is not a callable type".format(typ)
    Layers=[]
    
    
    #creating our layers of conditions
    for key,act in cases.items():
        my_key=key
        if not check_type(typ,my_key):
            print(TypeError,"Key {} should be type {} but is type {} instead".format(key,typ,type(key)) )
            return TypeError
        Layers.append([make_condition(key),act])
    
    #constructing the switch
    def construct_switch(input_value):
        """
        The switch is constrcuted as a couch of if layers where each leads to an action.
        Condition is a fonction that takes input value as parameters
        :param input_value: value who has same type as specified above
        :return: The action to make
        """
        #checking input type
        if not check_type(typ,input_value):
            return ValueError,"switch type value is {}".format(typ)
        
        #checking each layer
        for layer in Layers:
            if layer[0](input_value):
                return  layer[1]
            else:
                pass 
        #returns default condition if no others works
        return default
    
    return construct_switch
        
s=switch(str,default="Can't understand your words sorry",cases={"Hi":"Hello World","Au revoir":"See ya folks!"})
a=s("Hi")


#switch with dicts
def switch_dict(typ, default, cases):
    """
    Supported types are:
        -int
        -str
     Features only equality case for now.
     
    :param type: The type of value who will be tested in the switch ( int, str, float ,bin ,list )
    :param default: The default action to take if other conditions are not done
    :param cases: value=action
    :return: A switch method to call
    """

    def check_type(kind, value):
        """Check a value type"""
        if type(value) is kind:
            return True
        else:
            return False

    # checking typ is a callable type
    if not callable(typ): return "{} is not a callable type".format(typ)
    Layers = dict()

    # creating our layers of conditions
    for key, act in cases.items():
        my_key = key
        if not check_type(typ, my_key):
            print(TypeError, "Key {} should be type {} but is type {} instead".format(key, typ, type(key)))
            return TypeError
        Layers[key] = act

    # constructing the switch
    def construct_switch(input_value):
        """
        The switch is constrcuted as a couch of if layers where each leads to an action.
        Condition is a fonction that takes input value as parameters
        :param input_value: value who has same type as specified above
        :return: The action to make
        """
        # checking input type
        if not check_type(typ, input_value):
            return ValueError, "switch type value is {}".format(typ)

        # checking each layer
        try:
            return Layers[input_value]
        except KeyError:
            return default

    return construct_switch
