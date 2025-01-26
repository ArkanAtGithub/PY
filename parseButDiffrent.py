import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# File path
file_path = '/home/arkan/Documents/output.txt'

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

# Plot the time-domain data and spectrogram in the same window
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

# Spectrogram plot
plt.subplot(2, 1, 2)  # 2 rows, 1 column, 2nd subplot
Pxx, freqs, bins, im = plt.specgram(data, NFFT=256, Fs=1/time_step, noverlap=128, cmap='viridis')
plt.colorbar(im).set_label('Intensity (dB)')
plt.title('Spectrogram')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency (Hz)')

# Adjust layout and show plots
plt.tight_layout()
plt.show()
