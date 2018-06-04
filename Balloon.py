import csv
import math
import matplotlib.pyplot as plt
from pyproj import Proj
import numpy as np
from mpl_toolkits.basemap import pyproj
from mpl_toolkits.basemap import Basemap


tstep = 10

def read_data(file):
    with open(file, 'r') as r:
        reader = csv.reader(r, delimiter = " ", skipinitialspace=True)

        dat = [r for r in reader]
        return dat

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
while CUR_HEIGHT < 35000:

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


print(round(CUR_POS_X), round(CUR_POS_Y))

axs = [p[0] for p in ascent_path]
ays = [p[1] for p in ascent_path]

dxs = [p[0] for p in descent_path]
dys = [p[1] for p in descent_path]


myProj = Proj("+proj=utm +zone=23K, +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
base_lat = 40.0150
base_lon = -105.2705

r_earth = 6378000
lat_lons = []
for p in ascent_path:
    new_latitude = base_lat + (p[1] / r_earth) * (180 / math.pi)
    new_longitude = base_lon + (p[0] / r_earth) * (180 / math.pi) / math.cos(base_lat * math.pi/180)
    lat_lons.append((new_latitude, new_longitude))

for p in descent_path:
    new_latitude = base_lat + (p[1] / r_earth) * (180 / math.pi)
    new_longitude = base_lon + (p[0] / r_earth) * (180 / math.pi) / math.cos(base_lat * math.pi/180)
    lat_lons.append((new_latitude, new_longitude))


wh = 50000
lat_urc = base_lat + (wh / r_earth) * (180 / math.pi)
lon_urc = base_lon + (wh / r_earth) * (180 / math.pi) / math.cos(base_lat * math.pi/180)

lat_llc = base_lat + (-wh / r_earth) * (180 / math.pi)
lon_llc = base_lon + (-wh / r_earth) * (180 / math.pi) / math.cos(base_lat * math.pi/180)

m = Basemap(projection='merc',
              llcrnrlat=lat_llc,llcrnrlon=lon_llc,
              urcrnrlat=lat_urc, urcrnrlon=lon_urc,
              resolution='l',
              suppress_ticks=False)
m.drawstates()
m.drawrivers()
m.fillcontinents(color='coral',lake_color='aqua')
m.drawmapboundary(fill_color='aqua')
bx, by = m(base_lon, base_lat)
pt = m.plot(bx, by, 'ko',zorder=100)
print(base_lat, base_lon)
lats = [x[0] for x in lat_lons]
lons = [x[1] for x in lat_lons]
x, y = m(lons, lats)

m.scatter(x, y, s=10, zorder=100)

plt.show()






