# -*- coding: utf-8 -*-

from utils import fit_and_plot_line

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def R_I_model(I, R0, const):
    return const * R0 / (const - (1e-3 * I) ** 2)


IV = [(0.05, 0.474), (0.5, 4.720), (0.6, 5.67), (0.7, 6.61), (0.8, 7.55),
      (0.9, 8.501), (1, 9.459), (2.5, 23.82), (2.6, 24.795), (2.2, 20.935), (2, 19), (1.8, 17.075), (1.6, 15.15),
      (1.5, 14.195), (1.3, 12.3), (1.2, 11.35), (1.1, 10.4), (25, 900), (-25, -901.4), (20, 506), (-20, -506),
      (15, 217), (-15, -217), (10, 110), (-10, -110), (5, 48.85), (-5, -48.9), (-1, -9.45), (23, 741), (-23, -742),
      (21, 586), (-21, -586), (19, 432), (-19, -433), (17, 301), (-17, -301)]

I, V = zip(*IV)
R = np.divide(V, I)
I = np.array(I)
V = np.array(V)

valid_R = [abs(R) < 16]
R = R[valid_R]
I = I[valid_R]
V = V[valid_R]

plt.figure(1)
plt.grid()
plt.scatter(I, V, c='k')
plt.gca().set_axisbelow(True)

plt.title('V(I)')
plt.xlabel('I[mA]')
plt.ylabel('V[mV]')

plt.figure(2)
# force it to be such that R(0)<=min(R), AKA R(0)~=R0
R0_fit, const_fit = curve_fit(R_I_model, I, R, bounds=((5, 0), (min(R), np.inf)))[0]
I_fit = np.linspace(min(I), max(I), 1000)
R_fit = R_I_model(I_fit, R0_fit, const_fit)

plt.grid()
plt.scatter(I, R, c='k')
plt.plot(I_fit, R_fit, c='m')

plt.gca().set_axisbelow(True)
plt.title('R(I)')
plt.xlabel('I[mA]')
plt.ylabel('R[Ohm]')

plt.figure(3)
I = np.array(I)
R_error = R - R_I_model(I, R0_fit, const_fit)

plt.grid()
plt.gca().set_axisbelow(True)
plt.scatter(I, R_error, c='k')

plt.title('R Error Graph')
plt.xlabel('I[mA]')
plt.ylabel('R Error[Ohm]')

plt.figure(4)
plt.gca().set_axisbelow(True)
plt.grid(True)
plt.title('$\mathbb{\Delta}$T(P)')
plt.xlabel('P[$\mu$J/s]')
plt.ylabel('c$\mathbb{\Delta}$T[°C]')

P = I * V
delta_R = R - min(R)
plt.scatter(P, delta_R, c='k', zorder=5)
fit_and_plot_line(P, delta_R, fig=4, plot_axes=False, c='m')

plt.show()
