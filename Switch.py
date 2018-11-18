import re


class Switch:
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
    _Layers = []
    _default = None

    def __init__(self, default, init_cases):
        """
        Gives a type name to the object <class '__main__.Switch'>.
        Defines your switch
        :param default: Default case of the switch
        :param init_cases: dictionnary holding the cases and actions
        """
        self.__class__ = type(self.__class__.__name__, (self.__class__,), {})
        self.switch = self.init_switch(default, init_cases)

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
            self._Layers.append([key, self._make_int_condition(key), item])

        return self.__construct_switch

    def __construct_switch(self, input_value):
        """
        The switch is constrcuted as a couch of if layers where each leads to an action.
        Condition is a fonction that takes input value as parameters
        :param input_value: value who has same type as specified above
        :return: The action to make
        """
        # checking input type
        if not self._check_type(int, input_value):
            return ValueError, "switch type value is {}".format(int)

        # checking each layer
        for layer in self._Layers:
            if layer[1](input_value):
                return layer[2]
            else:
                pass
                # returns default condition if no others works
        return self._default

    def add_cases(self, add_cases):
        """
        Allows you to add cases to the switch
        :param add_cases: dictionnary of cases to add
        :return:nothing
        """
        for key, item in add_cases.items():
            self._Layers.append([key, self._make_int_condition(key), item])

    def remove_cases(self, key):
        """
        Allows you to remove cases until there is at least one condition
        remaining in addtion to default one
        :param key: key of the condtion to remove
        :return: nothing
        """
        if len(self._Layers) > 1:
            for item in self._Layers:
                if item[0] == key:
                    self._Layers.remove(item)
                    break

    def _make_int_condition(self, key):
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
        for i, item in enumerate(possible_exp):
            if re.match(item, key) is not None:
                values = re.findall("([-]?[0-9]+)", key)
                # double inequalities
                if i == 0: return lambda x: x in range(int(values[0]) + 1, int(values[1]))
                if i == 1: return lambda x: x in range(int(values[0]), int(values[1]))
                if i == 2: return lambda x: x in range(int(values[0]) + 1, int(values[1]) + 1)
                if i == 3: return lambda x: x in range(int(values[0]), int(values[1]) + 1)
                # equality
                if i == 4: return lambda x: x == int(values[0])
                # simple inequality
                if i == 5: return lambda x: x < int(values[0])
                if i == 6: return lambda x: x <= int(values[0])
                if i == 7: return lambda x: x > int(values[0])
                if i == 8: return lambda x: x >= int(values[0])

        return KeyError

    def _check_type(self, kind, value):
        """Check a value type"""
        try:
            kind(value)
            return True
        except ValueError:
            return False


cases = {"0<<12": lambda: print("0_12"), "=13": lambda: print(13), ">=14": lambda: print("14 et +")}
s = Switch(default=lambda: print('ok'), init_cases=cases)
s(5)()
s(-5)()
s.add_cases({"=-5": lambda: print("Added successfully")})
s(-5)()
s.remove_cases("=-5")
s(-5)()
print(type(s))
