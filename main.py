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
    y = f(x).real
    f1 = float(first_derivative(f,x))
    f2 = float(second_derivative(f,x))

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
    uy = f(x-h).real - cy

    vx = (x+h) - cx
    vy = f(x+h).real - cy

    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy

    ang = math.atan2(abs(cross), dot)

    return ang

def circle_arc_length_approx(f, x_i, x_f, h=1e-4):
    n = math.ceil((x_f-x_i)/(2*h))
    dx = (x_f-x_i) / n
    l = 0
    for i in range(n):
        x = x_i + (i +0.5)*dx
        circle = circle_geo(f,x)
        if circle["center"] is None:
            x1 = x - dx/2
            x2 = x + dx/2

            y1 = f(x - dx/2).real
            y2 = f(x + dx/2).real

            length = math.sqrt((x1-x2)**2 + (y1-y2)**2)

            l += length
            continue
        x, y = circle["point"]
        cx, cy = circle["center"]
        r = circle["radius"]
        ang = angle_find(cx, x, cy, dx/2)
        l += r*ang

    return l

def trad_arc_length_approx(f, x_i, x_f, h=1e-4):
    n = math.ceil((x_f-x_i)/(2*h))
    dx = (x_f-x_i) / n
    l = 0
    for i in range(n):
        x = x_i + (i +0.5)*dx
        l_func = math.sqrt(1+(first_derivative(f,x))**2)
        l += l_func * dx
    return l

func_string = input("Enter function (as python code, MUST USE cmath for special functions):")
h_values = [
    1e-1,
    5e-2,
    1e-2,
    5e-3,
    1.5e-3,
    1.25e-3,
    1e-3,
    9e-4,
    8e-4,
    7e-4,
    6e-4,
    5e-4,
    1e-4
]
for h in h_values:
    print(h)
    print(func_string)
    print(circle_arc_length_approx(f, 0, 2, h))
    print(trad_arc_length_approx(f, 0, 2, h))
    print("\n")
