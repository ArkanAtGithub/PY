import numpy as np
import matplotlib.pyplot as plt
from math import *
from scipy.signal import find_peaks
import time as counter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Define the GUI application class
class FFTApp:
    def __init__(self, root):
        self.root = root
        root.title("FFT Analysis GUI")
        root.geometry('500x500')  # Adjusted size to accommodate new widget
        root.resizable(width=False, height=False)

        # Create and place widgets
        self.label = tk.Label(root, text="Select a data file:")
        self.label.pack(pady=10)

        self.file_path_label = tk.Label(root, text="No file selected", fg="red")
        self.file_path_label.pack(pady=5)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        # Zero padding dropdown menu
        self.padding_label = tk.Label(root, text="Select Zero Padding:")
        self.padding_label.pack(pady=5)

        self.padding_var = tk.StringVar(root)
        self.padding_var.set("8")  # Default value
        self.padding_menu = tk.OptionMenu(root, self.padding_var, "1", "2", "4", "8", "16", "32", "64", "128", "256")
        self.padding_menu.pack(pady=5)

        # Peak threshold percentage input
        self.threshold_var = tk.StringVar(root)
        self.threshold_var.set("10")  # Default threshold percentage

        self.prominence_var = tk.StringVar(root)
        self.prominence_var.set("5")  # Default prominence percentage

        # Register the validation callback
        vcmd = (root.register(self.callback))

        # Entry with validation
        self.threshold_label = tk.Label(root, text="FFT Peak Threshold (% of max amplitude):")
        self.threshold_label.pack(pady=5)
        self.threshold_entry = tk.Entry(root, textvariable=self.threshold_var, validate='all', validatecommand=(vcmd, '%P'))
        self.threshold_entry.pack(pady=5)
        self.prominence_label = tk.Label(root, text="Prominence Threshold (% of max amplitude):")
        self.prominence_label.pack(pady=5)
        self.prominence_entry = tk.Entry(root, textvariable=self.prominence_var, validate='all', validatecommand=(vcmd, '%P'))
        self.prominence_entry.pack(pady=5)


        self.log_var = tk.StringVar(root)
        self.log_var.set("linear")
        self.log_amplitude = tk.Checkbutton(root, text="Log amplitude", variable=self.log_var, onvalue="log", offvalue="linear")
        self.log_amplitude.pack(pady=5)

        self.plot_button = tk.Button(root, text="Generate Plot", command=self.generate_plot)
        self.plot_button.pack(pady=5)

        self.time_taken_label = tk.Label(root, text="Time taken to generate figure: Not available")
        self.time_taken_label.pack(pady=5)

        self.file_path = ""

    def callback(self, P):
        # Allow empty input (to clear the field)
        if P == "":
            return True
        
        # Check if input is a valid decimal number
        try:
            value = float(P)
        except ValueError:
            return False

        # Ensure that value is within the range and contains only one '.'
        if 0 <= value <= 100 and P.count('.') <= 1:
            return True
        else:
            return False

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select data file",
            filetypes=[("Text files", "*.txt")]
        )
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a file to proceed.")
            self.file_path_label.config(text="No file selected", fg="red")
        else:
            self.file_path_label.config(text=f"File selected: {self.file_path}", fg="black")

    def generate_plot(self):
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a file to proceed.")
            return

        a = counter.time()

        try:
            # Read the file and extract the data
            with open(self.file_path, 'r') as file:
                first_line = file.readline().strip()
                lines = file.readlines()
        except:
            messagebox.showerror("File Error", f"No file found! Path: '{self.file_path}'")
            return

        # Time step detection
        try:
            time_step_value = float(first_line.split('=')[1].split()[0])
        except:
            messagebox.showerror("Wrong file", "Could not identify the first line.\n Wrong or corrupted file!")
            return
        time_step = float(time_step_value)

        # Skip the first line and convert the rest to floats
        data = np.array([float(line.strip()) for line in lines[1:]])

        # Generate the time array
        time = np.arange(0, len(data) * time_step, time_step)

        # Apply windowing
        def hamming_window(N):
            return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(N) / (N - 1))

        window = hamming_window(len(data))
        windowed_data = data * window

        # Get selected zero padding value from dropdown
        padding_multiplier = int(self.padding_var.get())
        n = len(windowed_data)
        n_padded = padding_multiplier * n
        fft_data = np.fft.fft(windowed_data, n=n_padded)
        fft_freq = np.fft.fftfreq(n_padded, d=time_step)

        # Only take the positive frequencies
        positive_freq_indices = fft_freq > 0
        fft_freq = fft_freq[positive_freq_indices]
        fft_data = np.abs(fft_data[positive_freq_indices])

        # Find peaks in the FFT data
        try:
            peak_threshold_percentage = float(self.threshold_var.get())
            prominence_percentage = float(self.prominence_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for threshold and prominence percentages.")
            return

        if not (0 <= peak_threshold_percentage <= 100) or not (0 <= prominence_percentage <= 100):
            messagebox.showerror("Input Error", "Both threshold and prominence percentages must be between 0 and 100.")
            return

        peak_threshold_value = (peak_threshold_percentage / 100) * np.max(fft_data)
        prominence_value = (prominence_percentage / 100) * np.max(fft_data)

        peaks, _ = find_peaks(fft_data, height=peak_threshold_value, distance=10, prominence=prominence_value)
        peak_height = np.full_like(fft_freq, peak_threshold_value)

        # Get the frequencies of the detected peaks
        peak_frequencies = fft_freq[peaks]

        # Sort peaks by amplitude (descending order)
        sorted_indices = np.argsort(fft_data[peaks])[::-1]
        sorted_peak_frequencies = peak_frequencies[sorted_indices]
        sorted_peak_amplitudes = fft_data[peaks][sorted_indices]

        # Plot the time-domain data and FFT data in the same window
        fig = plt.figure(figsize=(12, 10))

        # Add figure title
        file_name = self.file_path.split('/')[-1]
        fig.suptitle(file_name, fontweight='bold')

        # Time-domain plot
        ax1 = plt.subplot(2, 1, 1)
        plt.plot(time, data)
        plt.title('Time vs Voltage')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage')
        plt.grid(True)

        # Create legend for time step
        time_step_legend = plt.Line2D([0], [0], color='w', label=f'Time step: {time_step} s')
        max_voltage_legend = plt.Line2D([0], [0], color='w', label=f'Max voltage: {np.max(data):.2f} V')
        min_voltage_legend = plt.Line2D([0], [0], color='w', label=f'Min voltage: {np.min(data):.2f} V')
        p2p_voltage_legend = plt.Line2D([0], [0], color='w', label=f'P2P voltage: {(np.max(data) - np.min(data)):.2f} V')
        rms_voltage = np.sqrt(np.mean(np.square(data)))
        rms_voltage_legend = plt.Line2D([0], [0], color='w', label=f'RMS voltage: {rms_voltage:.2f} V')
        ax1.legend(handles=[time_step_legend, max_voltage_legend, min_voltage_legend, p2p_voltage_legend, rms_voltage_legend], loc='upper right', title='Signal Information', 
                   bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize='small')

        # Frequency-domain (FFT) plot
        ax2 = plt.subplot(2, 1, 2)
        plt.plot(fft_freq, fft_data, label='FFT Amplitude')
        plt.plot(fft_freq, peak_height, '--', label="Peak(s) Threshold")

        # Plot peaks and create legend entries for each peak
        peak_labels = []
        for freq, amp in zip(sorted_peak_frequencies, sorted_peak_amplitudes):
            plt.plot(freq, amp, 'r^')
            peak_labels.append(f'{freq:.2f} Hz')

        plt.title('Frequency vs Amplitude')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.xscale("log")
        plt.yscale(self.log_var.get())
        plt.grid(True, which="both")

        # Create legend with peak frequencies
        handles, labels = ax2.get_legend_handles_labels()
        handles.append(plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='r', markersize=10, label='Peak(s):'))
        for label in peak_labels:
            handles.append(plt.Line2D([0], [0], marker='', color='w', label=label))

        # Place legend inside the plot
        ax2.legend(handles=handles, loc='upper right', title='FFT plot', 
                   bbox_to_anchor=(1, 1), bbox_transform=ax2.transAxes, fontsize='small')

        b = counter.time()
        time_taken = b - a
        self.time_taken_label.config(text=f"Time taken: {time_taken:.6f} seconds")

        # Adjust layout and show plots
        plt.tight_layout()
        plt.show()

# Create the main window
root = tk.Tk()
app = FFTApp(root)
root.mainloop()
