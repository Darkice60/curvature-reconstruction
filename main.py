import math
import cmath
#import matplotlib

#Ask user for function and define it

def f(x):
    return eval(func_string, {"x": x, "math": math, "cmath": cmath})

def first_derivative(f, x, h=1e-20):
    return f(x+1j*h).imag/h

def second_derivative(f, x, h=1e-5):
    return 2*(f(x).real-f(x+1j*h).real)/h**2

def curvature(f, x):
    return ((second_derivative(f,x))/((1+(first_derivative(f,x))**2)**(1.5)))

def radius_of_curve(f,x):
    if (abs(second_derivative(f,x)) < 1e-10):
        return math.inf
    return (((1+(first_derivative(f,x))**2)**(1.5))/(second_derivative(f,x)))

func_string = input("Enter function (as python code, MUST USE cmath for special functions):")

x = eval(input("x=? "), {"math": math, "cmath": cmath})
deri_val = first_derivative(f, x)
deri2_val = second_derivative(f, x)
print(deri_val, deri2_val.real, curvature(f, x))