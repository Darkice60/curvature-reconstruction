from mpmath import mp

mp.dps = 80

def true_arc_length(f, func_string, x_i, x_f):
    def f(x):
        return eval(func_string, {"x": x, "math": mp, "cmath": mp})
    deri = lambda x: mp.diff(f, x)
    integrand = lambda x: mp.sqrt(1+(deri(x))**2)
    return mp.quad(integrand, [x_i, x_f])

def true_line_int(func_string, xt_string, yt_string, t_i, t_f):
    def f(x, y):
        return eval(func_string, {"x": x, "y": y, "math": mp, "cmath": mp})

    def xt(t):
        return eval(xt_string, {"t": t, "math": mp, "cmath": mp})

    def yt(t):
        return eval(yt_string, {"t": t, "math": mp, "cmath": mp})

    deri_x = lambda t: mp.diff(xt, t)
    deri_y = lambda t: mp.diff(yt, t)
    integrand = lambda t: f(xt(t), yt(t)) * mp.hypot(deri_x(t), deri_y(t))
    return mp.quad(integrand, [t_i, t_f])