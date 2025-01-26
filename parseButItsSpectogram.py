import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from math import *
from scipy.signal import spectrogram
import time as counter
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Define the GUI application class
class SpectrogramApp:
    def __init__(self, root):
        self.root = root
        root.title("Spectrogram Analysis GUI")
        root.geometry('500x600')  # Increased height to accommodate new options
        root.resizable(width=False, height=False)

        # Create and place widgets
        self.label = tk.Label(root, text="Select a data file:")
        self.label.pack(pady=10)

        self.file_path_label = tk.Label(root, text="No file selected", fg="red")
        self.file_path_label.pack(pady=5)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        # Spectrogram parameters
        self.nperseg_label = tk.Label(root, text="Segment Length:")
        self.nperseg_label.pack(pady=5)

        self.nperseg_var = tk.StringVar(root)
        self.nperseg_var.set("256")  # Default value
        self.nperseg_menu = tk.OptionMenu(root, self.nperseg_var, "64", "128", "256", "512", "1024", "2048", "4096")
        self.nperseg_menu.pack(pady=5)

        # Colormap selection
        self.colormap_label = tk.Label(root, text="Select Colormap:")
        self.colormap_label.pack(pady=5)

        self.colormap_var = tk.StringVar(root)
        self.colormap_var.set("viridis")  # Default colormap
        self.colormap_menu = tk.OptionMenu(root, self.colormap_var, 
                                           "viridis", "plasma", "inferno", "magma", 
                                           "cividis", "jet", "rainbow", "coolwarm")
        self.colormap_menu.pack(pady=5)

        # Scale types (Intensity and Frequency)
        self.intensity_scale_var = tk.StringVar(root)
        self.intensity_scale_var.set("linear")
        self.intensity_scale_label = tk.Label(root, text="Intensity Scale:")
        self.intensity_scale_label.pack(pady=5)
        self.intensity_linear_radio = tk.Radiobutton(root, text="Linear", variable=self.intensity_scale_var, value="linear")
        self.intensity_linear_radio.pack()
        self.intensity_log_radio = tk.Radiobutton(root, text="Logarithmic", variable=self.intensity_scale_var, value="log")
        self.intensity_log_radio.pack()

        # Frequency scale selection
        self.freq_scale_var = tk.StringVar(root)
        self.freq_scale_var.set("linear")
        self.freq_scale_label = tk.Label(root, text="Frequency Scale:")
        self.freq_scale_label.pack(pady=5)
        self.freq_linear_radio = tk.Radiobutton(root, text="Linear", variable=self.freq_scale_var, value="linear")
        self.freq_linear_radio.pack()
        self.freq_log_radio = tk.Radiobutton(root, text="Logarithmic", variable=self.freq_scale_var, value="log")
        self.freq_log_radio.pack()

        # Max Frequency Limit
        self.max_freq_label = tk.Label(root, text="Max Frequency Limit (k, M, G):")
        self.max_freq_label.pack(pady=5)
        self.max_freq_var = tk.StringVar(root)
        self.max_freq_var.set("auto")
        self.max_freq_entry = tk.Entry(root, textvariable=self.max_freq_var)
        self.max_freq_entry.pack(pady=5)

        self.plot_button = tk.Button(root, text="Generate Spectrogram", command=self.generate_spectrogram)
        self.plot_button.pack(pady=5)

        self.time_taken_label = tk.Label(root, text="Time taken to generate figure: Not available")
        self.time_taken_label.pack(pady=5)

        self.file_path = ""

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

    def generate_spectrogram(self):
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a file to proceed.")
            return

        a = counter.time()

        # Read and process file
        try:
            with open(self.file_path, 'r') as file:
                first_line = file.readline().strip()
                lines = file.readlines()
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading file: {e}")
            return

        try:
            time_step_value = float(first_line.split('=')[1].split()[0])
        except:
            messagebox.showerror("Wrong file", "Could not identify the first line.\n Wrong or corrupted file!")
            return

        time_step = float(time_step_value)
        data = np.array([float(line.strip()) for line in lines[1:]])
        time = np.arange(0, len(data) * time_step, time_step)
        nperseg = int(self.nperseg_var.get())
        f, t, Sxx = spectrogram(data, fs=1/time_step, nperseg=nperseg)

        # Parse max frequency with unit support
        try:
            freq_input = self.max_freq_var.get().strip().lower()
            unit = self.max_freq_var.get().strip().strip("0123456789")
            unit_map = {'k': 1e3, 'M': 1e6, 'G': 1e9}

            if freq_input == "auto":
                max_freq = f[-1]
            elif freq_input == "":
                self.max_freq_var.set("auto")
                return
            elif unit in unit_map:
                max_freq = float(freq_input[:-1]) * unit_map[unit]
            else:
                max_freq = float(freq_input)

            f_mask = f <= max_freq
            if self.freq_scale_var.get() == "log":
                f_mask &= (f > 0)

            f_filtered = f[f_mask]
            Sxx_filtered = Sxx[f_mask, :]
        except ValueError:
            messagebox.showerror("Input Error", "Invalid max frequency.\nUse a number optionally followed by 'k', 'M', or 'G'.")
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

        # Compute spectrogram
        nperseg = int(self.nperseg_var.get())
        f, t, Sxx = spectrogram(data, fs=1/time_step, nperseg=nperseg)

        # Plot the time-domain data and Spectrogram in the same window
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
        ax1.legend(handles=[time_step_legend, max_voltage_legend, min_voltage_legend, p2p_voltage_legend, rms_voltage_legend], 
                   loc='upper right', title='Signal Information', 
                   bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes, fontsize='small')

        # Spectrogram plot
        ax2 = plt.subplot(2, 1, 2)

        # Determine scaling based on user selection
        if self.intensity_scale_var.get() == "log":
            # Replace zero or negative values with a small positive number for LogNorm
            Sxx_filtered[Sxx_filtered <= 0] = 1e-10  # Small positive value
            norm = LogNorm(vmin=np.min(Sxx_filtered), vmax=np.max(Sxx_filtered))
        else:
            norm = plt.Normalize()

        # Plot spectrogram with selected colormap and frequency scaling
        if self.freq_scale_var.get() == "log":
            # Logarithmic frequency scale
            im = plt.pcolormesh(t, np.log10(f_filtered), 10 * np.log10(Sxx_filtered), 
                                shading='gouraud', 
                                cmap=self.colormap_var.get(), 
                                norm=norm)
            # Custom tick formatting for log scale
            ticks = plt.gca().get_yticks()
            plt.gca().set_yticklabels([f'{10**y:.1f}' for y in ticks])
            plt.ylabel('Frequency (Hz, log scale)')
        else:
            # Linear frequency scale
            im = plt.pcolormesh(t, f_filtered, 10 * np.log10(Sxx_filtered), 
                                shading='gouraud', 
                                cmap=self.colormap_var.get(), 
                                norm=norm)
            plt.ylabel('Frequency (Hz)')

        plt.colorbar(im, ax=ax2, label='Power/Frequency (dB/Hz)')
        plt.title('Spectrogram')
        plt.xlabel('Time (seconds)')

        b = counter.time()
        time_taken = b - a
        self.time_taken_label.config(text=f"Time taken: {time_taken:.6f} seconds")

        # Adjust layout and show plots
        plt.tight_layout()
        plt.show()

# Create the main window
root = tk.Tk()
app = SpectrogramApp(root)
root.mainloop()