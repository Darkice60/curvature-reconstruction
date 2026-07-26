import math
import cmath

def create_func(func_string):
    def f(x):
        return eval(func_string, {"x": x, "math": math, "cmath": cmath})
    return f