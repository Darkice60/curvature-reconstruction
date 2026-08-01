# curvature-reconstruction

A numerical exploration of approximating arc length and line integrals with osculating circles.

## Purpose

This project explores arc length approximations approximated with a midpoint Riemann sum and osculating circles.
It also seeks to compare line integrals with the aforementioned methods.

## Objective

- Compare calculated arc lengths
- Investigate line integrals along the approximated curve
- Analyze approximation error

## Important Info

This is all local, just download the files and run in the same folder.
You can change the range of step sizes by editing h-values.

In this project:
Circle refers to the osculating circle approximation value/function.
Line refers to the "traditional" line segement Riemann sum.
True refers to the true value of the arc length or line integral (determined by 'mpmath' to 80 dp for calculations).

### Acronyms

CLD stands for Circle-Line Difference,
CTE stands for Circle-True Error,
LTE stands for Line-True Error.

## Mathematics

Please refer to [Curvature Reconstruction Analysis](report/Curvature_Reconstruction_Analysis.pdf)

## Dependencies

- Python 3
- mpmath

The implementation is restricted to sufficiently smooth curves, since the method relies on first- and second-order derivative information.

## Current Status

Project complete. No further updates.

## License

MIT