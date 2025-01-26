import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# Given data points
x_data = np.array([3976, 3688, 3372, 3039, 2705, 2427, 2125, 1855, 1579, 1341, 1122, 952, 781, 668, 568, 488, 425, 383, 345, 316, 290, 269, 252, 238, 225, 217, 209, 202, 196])
y_data = np.array([1.5 ,1.8 ,2.2 ,2.7 ,3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82, 100, 120, 150, 180, 220, 270, 330])
# Actual data from test
x_test = np.array([3523, 2864, 613, 231, 212, 200])
y_test = np.array([2, 3, 20, 135, 200, 300])

estimate = 2864
try:
    y_true = y_test[x_test == estimate][0]
except:
    print("No such value in test data")
    exit()

def power_law(x, a, b):
    return a * x**b

def calculate_error(y_true, y_pred):
    error = abs(y_pred - y_true)
    error_percentage = (error / y_true) * 100
    return error, error_percentage

# 1. Original power law fit with error handling
try:
    params, _ = curve_fit(power_law, x_data, y_data, p0=[1000, -1], maxfev=10000)
    a, b = params
    y_original = power_law(estimate, a, b)
except RuntimeError as e:
    print(f"Error in original fit: {e}")
    y_original = None

# 2. Log-transformed linear fit
log_x = np.log(x_data)
log_y = np.log(y_data)
coeffs = np.polyfit(log_x, log_y, 1)
a_log, b_log = np.exp(coeffs[1]), coeffs[0]
y_log = power_law(estimate, a_log, b_log)

# 3. Piecewise linear interpolation
f_linear = interp1d(x_data, y_data)
y_linear = f_linear(estimate)

# 4. Cubic spline interpolation
f_cubic = interp1d(x_data, y_data, kind='cubic')
y_cubic = f_cubic(estimate)

print("-" * 70)
print(f"{'Value to estimate:':<20} {estimate}")
print(f"{'Correct estimation:':<20} {y_true}uF")
print("-" * 70)
print(f"{'Method':<20} | {'Estimated Value':<15} | {'Error':<10} | {'Error Percentage':<15}")
print("-" * 70)
if y_original is not None:
    print(f"{'Power law':<20} | {y_original:<15.3f} | {calculate_error(y_true, y_original)[0]:<10.3f} | {calculate_error(y_true, y_original)[1]:<15.3f}%")
print(f"{'Log-transformed':<20} | {y_log:<15.3f} | {calculate_error(y_true, y_log)[0]:<10.3f} | {calculate_error(y_true, y_log)[1]:<15.3f}%")
print(f"{'Linear Interp':<20} | {y_linear:<15.3f} | {calculate_error(y_true, y_linear)[0]:<10.3f} | {calculate_error(y_true, y_linear)[1]:<15.3f}%")
print(f"{'Cubic Spline':<20} | {y_cubic:<15.3f} | {calculate_error(y_true, y_cubic)[0]:<10.3f} | {calculate_error(y_true, y_cubic)[1]:<15.3f}%")
print("-" * 70)
