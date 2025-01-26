import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Given data points
x_data = np.array([4090, 3976, 3688, 3372, 3039, 2705, 2427, 2125, 1855, 1579, 1341, 1122, 952, 781, 668, 568, 488, 425, 383, 345, 316, 290, 269, 252, 238, 225, 217, 209, 202, 196])
y_data = np.array([1.4, 1.5 ,1.8 ,2.2 ,2.7 ,3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330])

# Ensure the lengths match
if len(x_data) != len(y_data):
    print(f"Lengths do not match: x_data has {len(x_data)} elements, y_data has {len(y_data)} elements.")
else:
    # Sort the data by x values
    sorted_indices = np.argsort(x_data)
    x_data_sorted = x_data[sorted_indices]
    y_data_sorted = y_data[sorted_indices]

    # Fit the cubic spline
    cs = CubicSpline(x_data_sorted, y_data_sorted)

    # Estimate the value at a specific point
    x_estimate = 4026
    y_estimate = cs(x_estimate)

    # Generate data for plotting the spline
    x_fit = np.linspace(min(x_data_sorted), max(x_data_sorted), 100)
    y_fit = cs(x_fit)

    # Plot the original data and the cubic spline
    plt.figure(figsize=(10, 6))
    plt.scatter(x_data_sorted, y_data_sorted, label='Data points')
    plt.plot(x_fit, y_fit, label='Cubic Spline Interpolation', color='red')
    plt.scatter(x_estimate, y_estimate, marker='^', color='green', label=f'Estimated capacitance: {y_estimate:.3f}uF')
    plt.xlabel('Raw ADC reading')
    plt.ylabel('Capacitance (uF)')
    plt.title('Raw ADC to Capacitance')
    plt.legend()
    plt.grid(True, which="both")
    plt.xscale("log")
    plt.yscale("log")
    plt.show()
