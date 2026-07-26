import math
import cmath
import exact_calcs

def create_func(func_string):
    def f(x):
        return eval(func_string, {"x": x, "math": math, "cmath": cmath})
    return f

def first_derivative(f, x, h=1e-30):
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

def angle_find(f, cx, x, cy, h):
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
        ang = angle_find(f, cx, x, cy, dx/2)
        l += r*ang

    return l

def line_arc_length_approx(f, x_i, x_f, h=1e-4):
    n = math.ceil((x_f-x_i)/(2*h))
    dx = (x_f-x_i) / n
    l = 0
    for i in range(n):
        x = x_i + (i +0.5)*dx
        l_func = math.sqrt(1+(first_derivative(f,x))**2)
        l += l_func * dx
    return l

def results(f, func_string, x_i, x_f, h):
    circ_val = circle_arc_length_approx(f, x_i, x_f, h)
    line_val = line_arc_length_approx(f, x_i, x_f, h)
    true_val = exact_calcs.true_arc_length(f, func_string, x_i, x_f)
    circ_line_diff = abs(circ_val - line_val)
    circ_true_error = abs(circ_val - true_val)
    line_true_error = abs(line_val - true_val)
    result = {
        "step": h,
        "circ": circ_val,
        "line": line_val,
        "true": true_val,
        "cld": circ_line_diff,
        "cte": circ_true_error,
        "lte": line_true_error
    }
    return result