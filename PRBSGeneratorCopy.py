import random
import time

time_a = time.time()
file_path = "/home/arkan/Documents/testOutput/bit.txt"
n_bit_list = 6  # Number of bits for sequence numbering
n_bit = 2       # Number of random bits per sequence
print_output = False
print("Pseudorandom binary sequence generator")
n = 0
last_bitstr = None  # To store the last generated sequence

# Ensure the output file starts empty
with open(file_path, 'w') as file:
    file.write("")

while n < 2**n_bit_list:
    c = format(n, f'0{n_bit_list}b')  # Generate the binary sequence number
    bitstr = None

    # Generate a new sequence until it's different from the last one
    while True:
        bit = [random.randint(0, 1) for _ in range(n_bit)]
        bitstr = ''.join(str(x) for x in bit)
        if bitstr != last_bitstr:
            break

    last_bitstr = bitstr  # Update the last generated sequence
    if print_output:
        print(f"{c}={bitstr}")
    
    # Write the result to the file
    with open(file_path, 'a') as file:
        file.write(f"{c}={bitstr}\n")
    
    n += 1

time_b = time.time()
print(f"Time taken: {time_b - time_a}s")