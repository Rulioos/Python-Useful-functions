# Useful-functions
A repository where i store some fonctions i made.
Feel free to give issue reports or to contribute with your own home made functions. 

# Switch.py
### Switch class 
Allows you to create a switch as in Java. It only takes care of int cases.
Create a switch in simple. 
Import Switch.py into your project.
Then create a switch as follows.
```python
cases = {"0<<12": lambda: print("0_12"), "=13": lambda: print(13), ">=14": lambda: print("14 et +")}
s = Switch(default=lambda: print('ok'), init_cases=cases, local_dict=locals())
```

You can **ADD** cases with a dict.If you add an existing case it will override it. 
As long as the switch has one case remaining you can **DELETE** a case like that.

```python
s.add_cases({"=-5": lambda: print("Added successfully")})
s.remove_cases("=-5")
```
### Ifmaker class
Allows you to creates int/float conditions ( for now  ) from regex. List of allowed regex is specified in comments.
You can create conditions with variables too but you'll need to initialize local_dict as locals()  or globals().


# Graph.py

Construct a simple graph.

# Diverse_functions
As it sounds , it's just small functions that may be useful sometimes.
