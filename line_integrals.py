# Darkice60
# line integral calculation file for curvature-reconstruction

#import math, cmath for special functions and mathematical constants
import math
import cmath
#import arc_length for derivative information
#import exact_calcs for exact line integral calculation
import arc_length
import exact_calcs

# function to create f(x, y) based on user input
def create_func(func_string):
    def f(x, y):
        return eval(func_string, {"x": x, "y": y, "math": math, "cmath": cmath})
    return f

# function to create x(t)/y(t) based on user input
def create_para(t_string):
    def f(t):
        return eval(t_string, {"t": t, "math": math, "cmath": cmath})
    return f

# function to package all geometric information of the osculating circle of (x(t),y(t))
def para_circle_geo(xt, yt, t):
     ## calculate x(t) and y(t) and the 1st and 2nd derivative at these values
    x = xt(t).real
    y = yt(t).real

    dx = arc_length.first_derivative(xt, t)
    dy = arc_length.first_derivative(yt, t)
    ddx = arc_length.second_derivative(xt, t)
    ddy = arc_length.second_derivative(yt, t)

    ## if the denominator of the radius function is 0 (< 1e-10 due to floating point)
    ## it implies the radius is infinite and that the is no circle
    if (abs(dx * ddy - dy * ddx) < 1e-10):
        ## return a dictionary reflecting this
        return {
            "point": (x, y),
            "center": None,
            "radius": math.inf,
            }

    ## calculate the radius of the osculating circle
    r = ((dx**2 + dy**2)**(1.5))/(dx * ddy - dy * ddx)

    ## calculate the cartesian center of the osculating circle
    cx = x - dy * (dx**2 + dy**2)/(dx * ddy - dy * ddx)
    cy = y + dx * (dx**2 + dy**2)/(dx * ddy - dy * ddx)

    ## return the point (x(t), y(t), the center of the osculating circle and its radius
    return {
        "point": (x, y),
        "center": (cx, cy),
        "radius": abs(r)
    }

# function to find the angle used to approximate the small circular arc used to approximate arc length for ds
## basically takes x(t +- h) and y(t +- h) and finds the angle between the and uses s = r * theta to get the length in circle_line_int_approx
def para_angle_find(xt, yt, t, cx, cy, h):
    ## create a vector u and its componets from the center to the point (x(t-h), y(t-h))
    ux = xt(t-h).real - cx
    uy = yt(t-h).real - cy

    ## create a vector v and its componets from the center to the point (x(t+h), y(t+h))
    vx = xt(t+h).real - cx
    vy = yt(t+h).real - cy

    ## calculate 2d scalar cross product and dot product of u and v
    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy

    ## calculate the angle between the 2 vectors with atan2
    ang = math.atan2(abs(cross), dot)

    ## return the angle
    return ang

# function to calc the approximate line integral of f(x,y) from t_i to t_f on <x(t), y(t)> by the method of osculating circles
def circle_line_int_approx(f, t_i, t_f, xt, yt, h=1e-4):
    ## calculate the number of steps needed and step size
    n = math.ceil((t_f-t_i)/(2*h))
    dt = (t_f-t_i) / n
    ## init integral value to 0
    inte = 0
    ## sum all curve pieces on the scalar field based on how many steps
    for i in range(n):
        ## set midpoint t value
        t = t_i + (i+0.5)*dt
        ## get osculating circle data
        circle = para_circle_geo(xt, yt, t)
        ## if there is no circle, fall back to line approximation
        if circle["center"] is None:
            ## create points for (x1, y1) and (x2, y2)
            x1 = xt(t - dt/2).real
            x2 = xt(t + dt/2).real

            y1 = yt((t - dt/2)).real
            y2 = yt((t + dt/2)).real

            ## calculate the distance between the 2 points for an approximate length
            length = math.hypot((x1-x2), (y1-y2))

            ## add segement value and continue loop
            inte += length * f(xt(t), yt(t))
            continue
        ## set values equal to dictionary values from para_circle_geo to use in anagle find
        x, y = circle["point"]
        cx, cy = circle["center"]
        r = circle["radius"]
        ang = para_angle_find(xt, yt, t, cx, cy, dt/2)
        ## multiply the radius by the ange to get a local arc length approx of the function, then by the value of the scalar field to actually approx the line int and add to total integral value
        inte += r*ang * f(xt(t), yt(t))
    ## return the line integral value
    return inte.real

# function to calc the approximate line integral of f(x,y) from t_i to t_f on <x(t), y(t)> by the method of line segements
def line_line_int_approx(f, t_i, t_f, xt, yt, h=1e-4):
    ## calculate the number of steps needed and step size
    n = math.ceil((t_f-t_i)/(2*h))
    dt = (t_f-t_i) / n
    ## init integral value to 0
    inte = 0
    ## sum all line segements on the scalar field based on how many steps
    for i in range(n):
        ## set midpoint t value
        t = t_i + (i+0.5)*dt
        ## declare integral function (which represents the local line segement at t) of sqrt([x'(t)]^2 + [y'(t)]^2) multiplied by the value of the scalar field at t
        inte_func = f(xt(t), yt(t)) * math.hypot(arc_length.first_derivative(xt, t), arc_length.first_derivative(yt, t))
        ## add to total integral value and continue loop
        inte += inte_func * dt
    ## return the line integral value
    return inte.real

# function to get arc length results for the users function and interval, and errors
def results(f, xt, yt, func_string, xt_string, yt_string, t_i, t_f, h):
    ## calculate the circle and line approximation
    circ_val = circle_line_int_approx(f, t_i, t_f, xt, yt, h)
    line_val = line_line_int_approx(f, t_i, t_f, xt, yt, h)
    ## calculate the true value of the line integral (to 80 dp)
    true_val = exact_calcs.true_line_int(func_string, xt_string, yt_string, t_i, t_f)
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