from mpmath import mp

mp.dps = 80

def true_arc_length(f, func_string, x_i, x_f):
    def f(x):
        return eval(func_string, {"x": x, "math": mp, "cmath": mp})
    deri = lambda x: mp.diff(f, x)
    integrand = lambda x: mp.sqrt(1+(deri(x))**2)
    return mp.quad(integrand, [x_i, x_f])