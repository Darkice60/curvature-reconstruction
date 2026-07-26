import math
import cmath
import arc_length
import line_integrals
#import matplotlib


choice = input("Choose Calculation:\nArc Length - 1\nPlaner Scaler Line Intergrals - 2")

if (choice == 1):
    func_string = input("Enter function of x (as python code, MUST USE cmath for special functions):")
    f = arc_length.create_func(func_string)

    x_i = eval(input("Enter the start of the interval: "), {"math": math, "cmath": cmath})
    x_f = eval(input("Enter the end of the interval: "), {"math": math, "cmath": cmath})

    h_values = [
        1e-1,
        5e-2,
        1e-2,
        5e-3,
        1.5e-3,
        1.2e-3,
        1e-3,
        9e-4,
        8e-4,
        7e-4,
        6e-4,
        5e-4,
        1e-4
    ]

    print("StepSize\tCircleVal\t\tLineVal\t\t\tTrueVal\t\t\tCLD\t\t\tCTE\t\t\tLTE")

    for h in h_values:
        result = arc_length.results(f, func_string, x_i, x_f, h)
        print(f'{(result["step"])}\t\t{result["circ"]:.12f}\t\t{result["line"]:.12f}\t\t{result["true"]:.12f}\t\t{result["cld"]:.12e}\t{result["cte"]:.12e}\t{result["lte"]:.12e}')
elif (choice == 2):
    func_string = input("Enter planer line as a function of x (as python code, MUST USE cmath for special functions):")
    f = line_integrals.create_func(func_string)
    func2_string = func_string = input("Enter function of x and y (as python code, MUST USE cmath for special functions):")
    g = line_integrals.create_func(func_string)
    x_i = eval(input("Enter the start of the interval: "), {"math": math, "cmath": cmath})
    x_f = eval(input("Enter the end of the interval: "), {"math": math, "cmath": cmath})
    
    h_values = [
        1e-1,
        5e-2,
        1e-2,
        5e-3,
        1.5e-3,
        1.2e-3,
        1e-3,
        9e-4,
        8e-4,
        7e-4,
        6e-4,
        5e-4,
        1e-4
    ]

    print("StepSize\tCircleVal\t\tLineVal\t\t\tTrueVal\t\t\tCLD\t\t\tCTE\t\t\tLTE")

    for h in h_values:
        result = arc_length.results(f, func_string, x_i, x_f, h)
        print(f'{(result["step"])}\t\t{result["circ"]:.12f}\t\t{result["line"]:.12f}\t\t{result["true"]:.12f}\t\t{result["cld"]:.12e}\t{result["cte"]:.12e}\t{result["lte"]:.12e}')