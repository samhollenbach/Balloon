import csv
import math
import matplotlib.pyplot as plt

tstep = 10

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
    return -(6 + 54*(h/30000.))



data = read_data("AtmoData.csv")

#print(data)
wind_speed = [0.514444*float(d[7]) for d in data]
#knots_conv =
#wind_speed = [v*knots_conv for v in wind_speed]

wind_degree = [math.pi * (int(d[6])+180)/180. for d in data]

heights = [int(d[1]) for d in data]


CUR_VERT_VEL = ascent_speed(0)

CUR_HORIZ_VEL = 0

CUR_HEIGHT = 0

CUR_POS_X = 0
CUR_POS_Y = 0

CUR_TIME = 0

ascent_path = []
descent_path = []
while CUR_HEIGHT < 33270:

    CUR_HEIGHT += ascent_speed(CUR_HEIGHT)*tstep
    height_index = 0
    while CUR_HEIGHT > heights[height_index]:
        height_index += 1
        if height_index >= len(heights):
            height_index -= 1
            break

    x_frac = math.sin(wind_degree[height_index])
    y_frac = math.cos(wind_degree[height_index])
    CUR_POS_X += wind_speed[height_index]*tstep*x_frac
    CUR_POS_Y += wind_speed[height_index]*tstep*y_frac
    ascent_path.append((CUR_POS_X,CUR_POS_Y))

    CUR_TIME += tstep

while CUR_HEIGHT > 0:

    CUR_HEIGHT += descent_speed(CUR_HEIGHT)*tstep
    height_index = 0
    while CUR_HEIGHT > heights[height_index]:
        height_index += 1
        if height_index >= len(heights):
            height_index -= 1
            break

    x_frac = math.sin(wind_degree[height_index])
    y_frac = math.cos(wind_degree[height_index])
    CUR_POS_X += wind_speed[height_index]*tstep*x_frac
    CUR_POS_Y += wind_speed[height_index]*tstep*y_frac
    descent_path.append((CUR_POS_X,CUR_POS_Y))

    CUR_TIME += tstep


print(CUR_POS_X, CUR_POS_Y)

axs = [p[0] for p in ascent_path]
ays = [p[1] for p in ascent_path]

dxs = [p[0] for p in descent_path]
dys = [p[1] for p in descent_path]

plt.plot(axs,ays, 'r.')
plt.plot(dxs,dys, 'b.')
plt.axis([0,50000,0,50000])
plt.show()





