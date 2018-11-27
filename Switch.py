import re


class IfMaker:
    """
    Class that takes a dict of local variables and allow you to define any int_condition with
    float,int and/or with variables in dict
    """

    def __init__(self, local_dict):
        """
        Initialize the existing variables dict
        :param local_dict: locals() or globals()
        """
        self.vars = local_dict

    def int_condition(self, key):
        """
        Creates equalities and inequalities from requests.
        :param key:Keys possibles shapes are:
            -"0<<12"
            -"0<=<=12"
            -">4" (same for < ) and "<=4"
            - "=4"
        :return: a function that holds the wanted condition
        """

        # regex of possibles expressions
        possible_exp = [r"(.)+<<(.)+", r"(.)+<=<(.)+", r"(.)+<<=(.)+", r"(.)+<=<=(.)+",
                        r"=(.)+", r"<(.)+", r"<=(.)+", r">(.)+", r">=(.)+"]

        def get_cond(index, tup_values):
            """
            :param index: Int between 0,8
            :param tup_values: a tuple ( inf,max )
            :return: a boolean function
            """
            # double inequalities
            if index == 0: return lambda x: (float(tup_values[0]) < x < float(tup_values[1]))
            if index == 1: return lambda x: (float(tup_values[0]) <= x < float(tup_values[1]))
            if index == 2: return lambda x: (float(tup_values[0]) < x <= float(tup_values[1]))
            if index == 3: return lambda x: (float(tup_values[0]) <= x <= float(tup_values[1]))
            # equality
            if index == 4: return lambda x: x == float(tup_values[0])
            # simple inequality
            if index == 5: return lambda x: x < float(tup_values[0])
            if index == 6: return lambda x: x <= float(tup_values[0])
            if index == 7: return lambda x: x > float(tup_values[0])
            if index == 8: return lambda x: x >= float(tup_values[0])

        for i, item in enumerate(possible_exp):
            if re.match(item, key) is not None:
                variables = re.findall("[-]?[a-z]+", key)
                nums = re.findall("([-]?[0-9]+)", key)
                for k in ["<<", "<=<", "<<=", "<=<="]:
                    if re.search(k, key) is None:
                        pass
                    else:
                        sep = k

                if len(variables) == 0:
                    return get_cond(i, nums)

                if len(nums) == 0:
                    values = []
                    try:
                        for var in variables:
                            var = float(self.vars[var])
                            values.append(var)
                    except NameError as e:
                        return e
                    return get_cond(i, values)
                else:
                    values = key.split(sep)
                    for v, var in enumerate(values):
                        if re.search("[a-z]+", var):
                            try:
                                var = float(self.vars[var])
                                values[v] = var
                            except NameError as e:
                                return e
                    return get_cond(i, values)

        return KeyError


class Switch(IfMaker):
    """
       Defines a switch class. You can create a switch whose type is  int and
       add conditions or remove conditions. Only the default condition is immutable.
       You must have 1 or more conditions at least too.
       An example of this switch :
           cases={"0<<12":lambda :print("0_12"),"=13":lambda :print(13),">=14":lambda : print("14 et +")}
           s=Switch(default=lambda :print('ok'),cases=cases)
           s(5)()
           s(13)()
       You can add conditions to the switch too.
           s.add_cases({"=-5": lambda: print("Added successfully")})
       You can remove some if there is at least one in plus of default one.
           s.remove_cases("=-5")
       """
    _Layers = dict()
    _default = None
    _conditions_keys = dict()
    switch = None

    def __init__(self, default, init_cases, local_dict):
        """
        Gives a type name to the object <class '__main__.Switch'>.
        Defines your switch
        :param default: Default case of the switch
        :param init_cases: dictionnary holding the cases and actions
        """
        super().__init__(local_dict)
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.init_switch(default, init_cases)

    def __call__(self, value):
        """
        Defines the call function so there is no need to call Switch.switch but just Switch(value to evaluate)
        :param value: Value to evaluate
        :return:
        """
        if self._check_type(int, value):
            return self.switch(value)
        else:
            return TypeError

    def init_switch(self, default, init_cases):
        """
        Initiating the first switch.
        Supported types are:
            -int
        :param default: The default action to take if other conditions are not done
        :param init_cases: Dict.Keys should have shape "0<<12","<12","=4",">14","0<=<12","0<<=12","0<=<=12".
                       Items could be anything.
        :return: A switch method to call
        """

        self._default = default
        for key, item in init_cases.items():
            cond = self.int_condition(key)
            self._Layers[cond] = item
            self._conditions_keys[key] = cond

        self.switch = self.__switch__

    def __switch__(self, arg):
        """Construct the switch"""
        for key, item in self._Layers.items():
            if key(arg):
                return item
        return self._default

    def add_cases(self, add_cases):
        """
        Allows you to add cases to the switch
        :param add_cases: dictionnary of cases to add
        :return:nothing
        """
        for key, item in add_cases.items():
            cond = self.int_condition(key)
            self._Layers[cond] = item
            self._conditions_keys[key] = cond

    def remove_cases(self, key):
        """
        Allows you to remove cases until there is at least one condition
        remaining in addtion to default one
        :param key: key of the condtion to remove
        :return: nothing
        """
        if len(self._Layers) > 1:
            if key in self._conditions_keys.keys():
                del self._Layers[self._conditions_keys[key]]
                return 0

    def _check_type(self, kind, value):
        """Check a value type"""
        try:
            kind(value)
            return True
        except ValueError:
            return False


cases = {"0<<12": lambda: print("0_12"), "=13": lambda: print(13), ">=14": lambda: print("14 et +")}
s = Switch(default=lambda: print('ok'), init_cases=cases, local_dict=locals())
s(5)()
s(-5)()
s.add_cases({"=-5": lambda: print("Added successfully")})
s(-5)()
s.remove_cases("=-5")
s(-5)()
print(type(s))
