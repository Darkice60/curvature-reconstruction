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

def circle_geo(f,x):
    y = f(x)
    f1 = first_derivative(f,x)
    f2 = second_derivative(f,x)

    if (abs(f2) < 1e-10):
        return {
                "point": (x, y),
                "center": None,
                "radius": math.inf,
                }

    cx = x - f1 * (1+f1**2)/f2
    cy = y + (1+f1**2)/f2

    r = abs((((1+(f1)**2)**(1.5))/(f2)))

    return {
        "point": (x, y),
        "center": (cx, cy),
        "radius": r,
        }

def angle_find(cx, x, cy, h):
    ux = (x-h) - cx
    uy = f(x-h) - cy

    vx = (x+h) - cx
    vy = f(x+h) - cy

    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy

    ang = math.atan2(abs(cross), dot)

    return ang

def circle_arc_length_approx(f, x_i, x_f, h=1e-4):
    x = x_i + h
    l = 0
    while(x < x_f):
        circle = circle_geo(f,x)
        x, y = circle["point"]
        cx, cy = circle["center"]
        r = circle["radius"]
        ang = angle_find(cx, x, cy, h)
        l += r*ang
        x += 2*h
    return l

def trad_arc_length_approx(f, x_i, x_f, h=1e-4):
    x = x_i + h
    l = 0
    while(x < x_f):
        l_func = math.sqrt(1+(first_derivative(f,x))**2)
        l += l_func * (2*h)
        x += 2*h
    return l

func_string = input("Enter function (as python code, MUST USE cmath for special functions):")
print(circle_arc_length_approx(f, 0, 4))
print(trad_arc_length_approx(f, 0, 4))