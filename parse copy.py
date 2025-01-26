import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.signal import find_peaks

# File path
file_path = '/home/arkan/Downloads/data-20240811-1426.circuitjs.txt'

try:
    # Read the file and extract the data
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        lines = file.readlines()
except:
    print(f"No file found! with path '{file_path}'")
    exit()

# Time step detection
time_step_value = float(first_line.split('=')[1].split()[0])
time_step = float(time_step_value)
ftsp = f"{time_step_value:.16f}"
print(f"Time step is {ftsp} second")
print(f"or {time_step_value} second")

# Skip the first line and convert the rest to floats
data = [float(line.strip()) for line in lines[1:]]

# Generate the time array
time = np.arange(0, len(data) * time_step, time_step)

# Perform FFT
n = len(data)
fft_data = np.fft.fft(data)
fft_freq = np.fft.fftfreq(n, d=time_step)

# Perform FFT with zero padding
n = len(data)
n_padded = 8 * n  # Increase the number of points by padding (e.g., 8 times)
fft_data = np.fft.fft(data, n=n_padded)
fft_freq = np.fft.fftfreq(n_padded, d=time_step)

# Only take the positive frequencies
positive_freq_indices = fft_freq > 0
fft_freq = fft_freq[positive_freq_indices]
fft_data = np.abs(fft_data[positive_freq_indices])

# Find peaks in the FFT data
peak_threshold_value = 0.25 * np.max(fft_data) # Set the peak threshold to be 1/4 the value
peaks, _ = find_peaks(fft_data, height=peak_threshold_value, prominence=1)
peak_height = np.full_like(fft_freq, peak_threshold_value)

# Plot the time-domain data and FFT data in the same window
fig = plt.figure(figsize=(12, 8))

# Add figure title
file_name_list = file_path.split('/')
file_name = file_name_list[-1]
fig.suptitle(file_name, fontweight='bold')

# Time-domain plot
plt.subplot(2, 1, 1)  # 2 rows, 1 column, 1st subplot
plt.plot(time, data, label=f'Time step {time_step}')
plt.title('Time vs Voltage')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage')
plt.grid(True)
plt.legend()

# Frequency-domain (FFT) plot
plt.subplot(2, 1, 2)  # 2 rows, 1 column, 2nd subplot
plt.plot(fft_freq, fft_data, label='FFT Amplitude')
plt.plot(fft_freq, peak_height, '--', label="Peak(s) Threshold")
plt.plot(fft_freq[peaks], fft_data[peaks], 'bo', label='Peak(s)')  # Mark peaks
plt.title('Frequency vs Amplitude')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xscale("log")
plt.grid(True)
plt.legend()

# Adjust layout and show plots
plt.tight_layout()
plt.show()
