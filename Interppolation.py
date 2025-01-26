import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Given data points
x_data = np.array([927, 789, 670, 560, 475, 390, 334, 284, 243, 212, 172, 158, 144, 134, 125, 119, 112, 108, 104, 101, 99])
y_data = np.array([5.6, 6.8, 8.2, 10, 12, 15, 18, 22, 27, 33, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330])

# Sort the data by x values
sorted_indices = np.argsort(x_data)
x_data_sorted = x_data[sorted_indices]
y_data_sorted = y_data[sorted_indices]

# Fit the cubic spline
cs = CubicSpline(x_data_sorted, y_data_sorted)

# Estimate the value at a specific point
x_estimate = 279
y_estimate = cs(x_estimate)
print(f"Estimated value at x = {x_estimate}: {y_estimate:.2f}")

# Generate data for plotting the spline
x_fit = np.linspace(min(x_data_sorted), max(x_data_sorted), 100)
y_fit = cs(x_fit)

# Plot the original data and the cubic spline
plt.figure(figsize=(10, 6))
plt.scatter(x_data_sorted, y_data_sorted, label='Data points')
plt.plot(x_fit, y_fit, label='Cubic Spline Interpolation', color='red')
plt.scatter(x_estimate, y_estimate, color='green', label=f'Estimate at x = {x_estimate}: {y_estimate:.2f}')
plt.xlabel('Raw ADC reading')
plt.ylabel('Capacitance (uF)')
plt.title('Cubic Spline Interpolation to Data')
plt.legend()
plt.ylim(bottom=0)
plt.grid(True)
plt.show()
