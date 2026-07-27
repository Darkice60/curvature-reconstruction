# Darkice60
# exact calculations file for curvature-reconstruction

#import mpmath for exact calculations
from mpmath import mp

# set accuracy to 80 dp
mp.dps = 80

# function to find the true arc length of f(x) on [x_i, x_f]
def true_arc_length(f, func_string, x_i, x_f):
    ## function to build the f(x) function
    def f(x):
        return eval(func_string, {"x": x, "math": mp, "cmath": mp})
    ## define the derivative of f(x) and the arc length integrand of f(x)
    deri = lambda x: mp.diff(f, x)
    integrand = lambda x: mp.sqrt(1+(deri(x))**2)
    ## return the arc length
    return mp.quad(integrand, [x_i, x_f])

# function to find the true line integral of f(x, y) on <x(t), y(t)> on [t_i, t_f]
def true_line_int(func_string, xt_string, yt_string, t_i, t_f):
    ## function to build the f(x, y) scalar field
    def f(x, y):
        return eval(func_string, {"x": x, "y": y, "math": mp, "cmath": mp})

    ## function to build the x(t) parameter
    def xt(t):
        return eval(xt_string, {"t": t, "math": mp, "cmath": mp})

    ## function to build the y(t) parameter
    def yt(t):
        return eval(yt_string, {"t": t, "math": mp, "cmath": mp})

    ## define the derivative of x(t) and y(t)
    deri_x = lambda t: mp.diff(xt, t)
    deri_y = lambda t: mp.diff(yt, t)
    ## define the integrand of the line integral
    integrand = lambda t: f(xt(t), yt(t)) * mp.hypot(deri_x(t), deri_y(t))
    ## return the line integral
    return mp.quad(integrand, [t_i, t_f])