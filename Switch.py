"""
Defines a python switch with all security measures around variable type. It's done without use of dictionnary but dictionnaries
maybe better than lists in that kind of problem. 
Two versions are distributed here:
    - A version that features only equality cases but int and str type
    - A version that features both equality and inequality cases but does only support int type
  
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

def check_type(kind, value):
    """Check a value type"""
    try:
        kind(value)
        return True
    except ValueError:
        return False
    
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




def make_int_condition(key):
    """
    Creates equalities and inequalities from requests.

    :param key:Keys possibles shapes are:
        -"0<<12"
        -"0<=<=12"
        -">4" (same for < ) and "<=4"
        - "=4"
    :return: a function that holds the wanted condition
    """

    #equality
    if key.startswith("="):
        if check_type(int,key[1:]):
            return lambda x: x == int(key[1:])
        else: return TypeError

    #Double inequalities
    if key.startswith("<") and check_type(int, key[1:]):
        return lambda x: x < int(key[1:])
    if key.startswith("<=") and check_type(int, key[2:]):
        return lambda x: x <= int(key[2:])
    if key.startswith(">") and check_type(int, key[1:]):
        return lambda x: x >int(key[1:])
    if key.startswith(">=") and check_type(int, key[2:]):
        return lambda x: x >= int(key[2:])

    #triple inequalities
    possible_exp=[r"(.)+<<(.)+",r"(.)+<=<(.)+",r"(.)+<<=(.)+",r"(.)+<=<=(.)+"]
    for i,item in enumerate(possible_exp):
        if re.match(item,key) is not None:
            Values=re.findall("([0-9]+)",key)
            if i == 0: return lambda x: x in range(int(Values[0])+1,int(Values[1]))
            if i == 1: return lambda x: x in range(int(Values[0]), int(Values[1]))
            if i == 2: return lambda x: x in range(int(Values[0]) +1, int(Values[1])+1)
            if i == 3: return lambda x: x in range(int(Values[0]), int(Values[1])+1)

    return KeyError





def switch_int(default, cases):
    """
    Supported types are:
        -int
     
    :param default: The default action to take if other conditions are not done
    :param cases: Dict.Keys should have shape "0<<12","<12","=4",">14","0<=<12","0<<=12","0<=<=12".
                   Items could be anything.
    :return: A switch method to call
    """
    Layers=[]
    for key,item in cases.items():
        Layers.append([make_int_condition(key),item])
    def construct_switch(input_value):
        """
        The switch is constrcuted as a couch of if layers where each leads to an action.
        Condition is a fonction that takes input value as parameters
        :param input_value: value who has same type as specified above
        :return: The action to make
        """
        # checking input type
        if not check_type(int, input_value):
            return ValueError, "switch type value is {}".format(int)

        # checking each layer
        for layer in Layers:
            if layer[0](input_value):
                return layer[1]
            else:
                pass
                # returns default condition if no others works
        return default


    return construct_switch

#exemples
cases={"0<<12":lambda :print("0_12"),"=13":lambda :print(13),">=14":lambda : print("14 et +")}
s=switch_int(default=lambda :print('ok'),cases=cases)
s(5)()
s(13)()
s(14)()
s(15)()
s(-1)()


