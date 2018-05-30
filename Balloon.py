import csv
import numpy as np


tstep = 1

def read_data(file):
    with open(file, 'r') as r:
        reader = csv.reader(r, delimiter = " ")

        dat = [r for r in reader]

        final_dat = []
        for d in dat:
            row = []
            for x in d:
                if x == '':
                    continue
                row.append(x)
            final_dat.append(row)
    return final_dat

# m/s
def ascent_speed(h=0):
    return 6

# m/s
def descent_speed(h):
    return 6 + 54*(h/30000.)

# kg * m/s
def drag_force(h, p, v, A = 1):
    return


data = read_data("AtmoData.csv")

print(data)





