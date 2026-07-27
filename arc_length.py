# Darkice60
# arc length calculation file for curvature-reconstruction

#import math, cmath for special functions and mathematical constantsimport math
import math
import cmath
#import exact_calcs for exact arc length calculation
import exact_calcs

# function to create f(x) based on user input
def create_func(func_string):
    def f(x):
        return eval(func_string, {"x": x, "math": math, "cmath": cmath})
    return f

# first derivative at a value x of f(x)
def first_derivative(f, x, h=1e-30):
    return f(x+1j*h).imag/h

# second derivative at a value x of f(x)
def second_derivative(f, x, h=1e-5):
    return 2*(f(x).real-f(x+1j*h).real)/h**2

# function to package all geometric information of the osculating circle of f at x
def circle_geo(f,x):
    ## calculate f(x) and the 1st and 2nd derivative at these values
    y = f(x).real
    f1 = float(first_derivative(f,x))
    f2 = float(second_derivative(f,x))

    ## if the second derivative is 0 (< 1e-10 due to floating point)
    ## it implies the radius is infinite and that the is no circle
    if (abs(f2) < 1e-10):
        ## return a dictionary reflecting this
        return {
                "point": (x, y),
                "center": None,
                "radius": math.inf,
                }

    ## calculate the cartesian center of the osculating circle
    cx = x - f1 * (1+f1**2)/f2
    cy = y + (1+f1**2)/f2

    ## calculate the radius of the osculating circle
    r = abs((((1+(f1)**2)**(1.5))/(f2)))

    ## return the point (x, f(x)), the center of the osculating circle and its radius
    return {
        "point": (x, y),
        "center": (cx, cy),
        "radius": r,
        }

# function to find the angle used to approximate the small circular arc used to approximate arc length
## basically takes x +- h and finds the angle between the and uses s = r * theta to get the length in circle_arc_length_approx
def angle_find(f, cx, x, cy, h):
    ## create a vector u and its componets from the center to the point (x-h, f(x-h))
    ux = (x-h) - cx
    uy = f(x-h).real - cy

    ## create a vector v and its componets from the center to the point (x+h, f(x+h))
    vx = (x+h) - cx
    vy = f(x+h).real - cy

    ## calculate 2d scalar cross product and dot product of u and v
    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy

    ## calculate the angle between the 2 vectors with atan2
    ang = math.atan2(abs(cross), dot)

    ## return the angle
    return ang

# function to get the approximate arc length of f(x) from x_i to x_f by the method of osculating circles
def circle_arc_length_approx(f, x_i, x_f, h=1e-4):
    ## calculate the number of steps needed and step size
    n = math.ceil((x_f-x_i)/(2*h))
    dx = (x_f-x_i) / n
    ## init length to 0
    l = 0
    ## sum all curve pieces based on how many steps
    for i in range(n):
        ## set midpoint x value
        x = x_i + (i +0.5)*dx
        ## get osculating circle data
        circle = circle_geo(f,x)
        ## if there is no circle, fall back to line approximation
        if circle["center"] is None:
            ## create points for (x1, y1) and (x2, y2)
            x1 = x - dx/2
            x2 = x + dx/2

            y1 = f(x - dx/2).real
            y2 = f(x + dx/2).real

            ## calculate the distance between the 2 points for an approximate length
            length = math.hypot((x1-x2), (y1-y2))

            ## add length and continue loop
            l += length
            continue
        ## set values equal to dictionary values from circle_geo to use in anagle find
        x, y = circle["point"]
        cx, cy = circle["center"]
        r = circle["radius"]
        ang = angle_find(f, cx, x, cy, dx/2)
        ## multiply the radius by the ange to get a local arc length approx of the function
        l += r*ang
    ## return the length
    return l

# function to get the approximate arc length of f(x) from x_i to x_f by the method of line segements
def line_arc_length_approx(f, x_i, x_f, h=1e-4):
    ## calculate the number of steps needed and step size
    n = math.ceil((x_f-x_i)/(2*h))
    dx = (x_f-x_i) / n
    ## init length to 0
    l = 0
    ## sum all line segements based on how many steps
    for i in range(n):
        ## set midpoint x value
        x = x_i + (i +0.5)*dx
        ## declare length function (which represents the local line segement at x) of sqrt(1 + [f'(x)]^2)
        l_func = math.sqrt(1+(first_derivative(f,x))**2)
        ## add to total length and continue loop
        l += l_func * dx
    ## return total length
    return l

# function to get arc length results for the users function and interval, and errors
def results(f, func_string, x_i, x_f, h):
    ## calculate the circle and line approximation
    circ_val = circle_arc_length_approx(f, x_i, x_f, h)
    line_val = line_arc_length_approx(f, x_i, x_f, h)
    ## calculate the true value of the arc length (to 80 dp)
    true_val = exact_calcs.true_arc_length(f, func_string, x_i, x_f)
    ## calculate CLD, CTE, LTE (see README.md)
    circ_line_diff = abs(circ_val - line_val)
    circ_true_error = abs(circ_val - true_val)
    line_true_error = abs(line_val - true_val)
    ## compile these results as a dictionary
    result = {
        "step": h,
        "circ": circ_val,
        "line": line_val,
        "true": true_val,
        "cld": circ_line_diff,
        "cte": circ_true_error,
        "lte": line_true_error
    }
    ## return the dictionary
    return result