import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def fit_func(func, x, y, p0=None, bounds=None):
    if bounds is not None:
        params_result, cov_mat = curve_fit(func, x, y, p0=p0, bounds=bounds)
    else:
        params_result, cov_mat = curve_fit(func, x, y, p0=p0)
    return params_result, np.sqrt(np.diag(cov_mat))


def fit_line(x, y):
    return fit_func(lambda z, a, b: a * z + b, x, y)


def plot_region(low_func, upper_func, x_range):
    x = np.linspace(x_range[0], x_range[1], 200)
    plt.fill_between(x, low_func(x), upper_func(x), facecolor='m', alpha=0.2)


def plot_func(func, x_range, **kwargs):
    x = np.linspace(x_range[0], x_range[1], 100)
    plt.plot(x, func(x), **kwargs)


def plot_line(slope, intercept, fig, x_range=None, plot_axes=True, c='k', linestyle='solid', linewidth=None,
              zorder=None):
    plt.figure(fig)
    plot_func(lambda x: slope * x + intercept, x_range, c=c, linestyle=linestyle, linewidth=linewidth, zorder=zorder)
    if plot_axes:
        plt.axhline(0, c='k')
        plt.axvline(0, c='k')


def plot_log_fit(R, T, fig, R_type):
    plt.figure(fig)
    [power, log_coefficient], errors = fit_line(np.log(T), np.log(R))

    plot_range = (min(T), max(T))

    plot_func(lambda x: np.exp(log_coefficient) * np.power(x, power), plot_range)
    # plot_region(lambda x: np.exp(log_coefficient - errors[1]) * np.power(x, power - errors[0]),
    #             lambda x: np.exp(log_coefficient + errors[1]) * np.power(x, power + errors[0]), plot_range)
    plt.scatter(T, R, c='g')
    plt.loglog()
    plt.minorticks_off()
    plt.yticks(np.linspace(round(0.9 * min(R), 0), round(1.05 * max(R), 0), 5))
    plt.xticks(np.linspace(round(plot_range[0], 0), round(plot_range[1], 0), 5))
    plt.grid(True, which='both')
    plt.xlabel('$\mathbb{\Delta}$T[°C]')
    plt.ylabel('R[$\mathbb{\Omega}$]')
#    plt.title(
#        '$R_{' + R_type + '}$' + '($\mathbb{\Delta}$T)=' + f'({np.exp(log_coefficient):.2f}$\pm${errors[0]:.2f})' +
#        '$(\mathbb{\Delta}$T)' + f'^({power:.2f}$\pm${errors[1]:.2f})')


def plot_half_log_fit(R, T, fig, R_type):
    plt.figure(fig)
    [log_base, log_coefficient], errors = fit_line(T, np.log(R))

    base, coefficient = np.exp([log_base, log_coefficient])
    coefficient_low_err = coefficient - np.exp(log_coefficient - errors[0])
    coefficient_high_err = np.exp(log_coefficient + errors[0]) - coefficient
    base_low_err = base - np.exp(log_base - errors[1])
    base_high_err = np.exp(log_base + errors[1]) - base

    plot_range = (min(T), max(T))

    plot_func(lambda x: coefficient * np.power(base, x), plot_range)
    plt.scatter(T, R, c='g')
    plt.semilogy()
    plt.minorticks_off()
    plt.yticks(np.linspace(round(0.9 * min(R), 0), round(1.05 * max(R), 0), 5))
    plt.xticks(np.linspace(round(plot_range[0], 0), round(plot_range[1], 0), 5))
    plt.grid(True, which='both')
    
#    coefficient_err_str = '$^{' + f'{coefficient_high_err:.2f}' + '}_{' + f'{coefficient_low_err:.2f}' + '}$'
#    base_err_str = '$^{' + f'{base_high_err:.2f}' + '}_{' + f'{base_low_err:.2f}' + '}$'

    plt.xlabel('$\mathbb{\Delta}$T[°C]')
    plt.ylabel('R[$\mathbb{\Omega}$]')
#    plt.title(
#        '$R_{' + R_type + '}$' + '($\mathbb{\Delta}$T)=' + f'({coefficient:.2f}$\pm$' + coefficient_err_str +
#        f')({base:.2f}$\pm$' + base_err_str + ')^$(\mathbb{\Delta}$T)')


def fit_and_plot_line(x, y, fig, x_range=None, plot_axes=False, c='k', linestyle='solid', linewidth=None, zorder=None):
    [slope, intercept], errors = fit_line(x, y)
    if x_range is None:
        x_range = [min(x), max(x)]
    plot_line(slope, intercept, fig, x_range, plot_axes, c=c, linestyle=linestyle, linewidth=linewidth, zorder=zorder)
    return [slope, intercept], errors


def wait_for_not_mouse_button_press():
    while not plt.waitforbuttonpress():
        continue
