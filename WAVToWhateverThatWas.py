import wave
import numpy as np

def wav_to_text(wav_file, output_file):
    # Open the WAV file
    with wave.open(wav_file, 'rb') as wav:
        # Extract audio parameters
        n_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        frame_rate = wav.getframerate()
        n_frames = wav.getnframes()

        # Read the audio data
        audio_data = wav.readframes(n_frames)

        # Calculate the expected buffer size based on the sample width
        expected_size = n_frames * n_channels * sample_width

        # Trim the buffer to ensure it is a multiple of the element size
        if len(audio_data) % sample_width != 0:
            audio_data = audio_data[:-(len(audio_data) % sample_width)]

        # Convert the buffer to a NumPy array based on the sample width
        if sample_width == 1:  # 8-bit samples
            dtype = np.uint8
        elif sample_width == 2:  # 16-bit samples
            dtype = np.int16
        elif sample_width == 4:  # 32-bit samples
            dtype = np.int32
        else:
            raise ValueError(f"Unsupported sample width: {sample_width} bytes")

        audio_data = np.frombuffer(audio_data, dtype=dtype)

        # If stereo, take the first channel
        if n_channels > 1:
            audio_data = audio_data[::n_channels]

        # Normalize audio data to range [-1, 1]
        max_value = np.iinfo(dtype).max
        audio_data = audio_data / max_value

        # Calculate the time step based on the sampling rate
        time_step = 1.0 / frame_rate

        # Write to the output file
        with open(output_file, 'w') as out_file:
            out_file.write("# time step = {} sec\n".format(time_step))
            for sample in audio_data:
                out_file.write("{}\n".format(sample))

if __name__ == "__main__":
    wav_file = "/home/arkan/Downloads/audio-20240813-2107.circuitjs.wav"  # Replace with your WAV file path
    output_file = "/home/arkan/Documents/output.txt"  # Replace with your desired output file path
    wav_to_text(wav_file, output_file)
