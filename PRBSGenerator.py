import random
import numpy as np
import time

time_a = time.time()
file_path = "/home/arkan/Documents/testOutput/bit.txt"
n_bit_list = 8
n_bit = 1
print_output = False
print("Pseudorandom binary sequence generator")
n = 0
with open(file_path, 'w') as file:
    file.write("")

while n < 2**n_bit_list:
    c = format(n, f'0{n_bit_list}b')
    bit = []
    for _ in range(n_bit):
        bit.append(random.randint(0, 1))
    
    bitstr = ''.join(str(x) for x in bit)
    if print_output == True:
        print(f"{c}={bitstr}")
    with open(file_path, 'a') as file:
        file.write(f"{c}={bitstr}\n")
    
    n += 1

time_b = time.time()
print(f"Time taken: {time_b - time_a}s")