import numpy as np

# Parameters
num_samples = 1024      # Number of samples in the sine wave
max_amplitude = 1024    # Full amplitude range
amplitude = (max_amplitude - 1) / 2  # Scale to max - 1
offset = amplitude                    # Offset to center the wave

# Generate sine wave
x = np.arange(num_samples)
sine_wave = (amplitude * np.sin(2 * np.pi * x / num_samples) + offset).astype(int)

# Convert to desired format
formatted_output = "0: " + " ".join(map(str, sine_wave))
print(formatted_output)
