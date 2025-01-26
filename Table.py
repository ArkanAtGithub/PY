from datetime import *
import csv

file_name = "test.csv"

time_now = datetime.now()
time_strf = time_now.strftime("%H:%M:%S %Y-%m-%d")

try:
    with open(file_name, "x") as f:
        f.write("TIME,AMOUNT\n")
        print(f'Creating file "{file_name}"')
except FileExistsError:
    print(f'Using file "{file_name}"')
except Exception as e:
    print(f"An error occurred: {e}")

usr_input = int(input("Amount(in IDR K): "))
proc_input = usr_input * 1000

inout = str(input("In or out [I/o]: ")).lower()

try:
    if inout == "o":
        proc_input = -abs(proc_input)
        print("OUT")
    else:
        print("IN")
        None
except:
    print("Something went wrong!")

str_input =f"Rp{proc_input:,.2f}"

with open(file_name, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([time_strf, str_input])

print("============")

with open(file_name, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        print(' '.join(row))
