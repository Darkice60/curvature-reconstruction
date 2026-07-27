import math
import cmath
import arc_length
import exact_calcs

def create_func(func_string):
    def f(x, y):
        return eval(func_string, {"x": x, "y": y, "math": math, "cmath": cmath})
    return f

def create_para(t_string):
    def f(t):
        return eval(t_string, {"t": t, "math": math, "cmath": cmath})
    return f

def para_circle_geo(xt, yt, t):
    x = xt(t).real
    y = yt(t).real

    dx = arc_length.first_derivative(xt, t)
    dy = arc_length.first_derivative(yt, t)
    ddx = arc_length.second_derivative(xt, t)
    ddy = arc_length.second_derivative(yt, t)

    if (abs(dx * ddy - dy * ddx) < 1e-10):
        return {
            "point": (x, y),
            "center": None,
            "radius": math.inf,
            }

    r = ((dx**2 + dy**2)**(1.5))/(dx * ddy - dy * ddx)

    cx = x - dy * (dx**2 + dy**2)/(dx * ddy - dy * ddx)
    cy = y + dx * (dx**2 + dy**2)/(dx * ddy - dy * ddx)

    return {
        "point": (x, y),
        "center": (cx, cy),
        "radius": abs(r)
    }

def para_angle_find(xt, yt, t, cx, cy, h):
    ux = xt(t-h).real - cx
    uy = yt(t-h).real - cy

    vx = xt(t+h).real - cx
    vy = yt(t+h).real - cy

    cross = ux * vy - uy * vx
    dot = ux * vx + uy * vy

    ang = math.atan2(abs(cross), dot)

    return ang

def circle_line_int_approx(f, t_i, t_f, xt, yt, h=1e-4):
    n = math.ceil((t_f-t_i)/(2*h))
    dt = (t_f-t_i) / n
    inte = 0
    for i in range(n):
        t = t_i + (i+0.5)*dt
        circle = para_circle_geo(xt, yt, t)
        if circle["center"] is None:
            x1 = xt(t - dt/2).real
            x2 = xt(t + dt/2).real

            y1 = yt((t - dt/2)).real
            y2 = yt((t + dt/2)).real

            length = math.hypot((x1-x2), (y1-y2))

            inte += length * f(xt(t), yt(t))
            continue
        x, y = circle["point"]
        cx, cy = circle["center"]
        r = circle["radius"]
        ang = para_angle_find(xt, yt, t, cx, cy, dt/2)
        inte += r*ang * f(xt(t), yt(t))
    return inte.real

def line_line_int_approx(f, t_i, t_f, xt, yt, h=1e-4):
    n = math.ceil((t_f-t_i)/(2*h))
    dt = (t_f-t_i) / n
    inte = 0
    for i in range(n):
        t = t_i + (i+0.5)*dt
        inte_func = f(xt(t), yt(t)) * math.hypot(arc_length.first_derivative(xt, t), arc_length.first_derivative(yt, t))
        inte += inte_func * dt
    return inte.real

def results(f, xt, yt, func_string, xt_string, yt_string, t_i, t_f, h):
    circ_val = circle_line_int_approx(f, t_i, t_f, xt, yt, h)
    line_val = line_line_int_approx(f, t_i, t_f, xt, yt, h)
    true_val = exact_calcs.true_line_int(func_string, xt_string, yt_string, t_i, t_f)
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


