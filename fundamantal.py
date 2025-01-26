while True:
    try:
        fundamental = float(input("Fundamental (Hz): "))
        break
    except ValueError:
        print("Error: Please enter a valid number.")

i = 1
even = []
odd = []
while i <= 10:
    i += 1
    if i % 2 == 0:
        even.append(fundamental * i)
    else:
        odd.append(fundamental * i)

for x, y in zip(even, odd):
    print(f"{i:<1}: {x:<10}{'|':<5}{y:<5}")
