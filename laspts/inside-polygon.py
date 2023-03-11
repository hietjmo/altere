
# python inside-polygon.py L4133B3.txt -N=6672509.414 -E=385221.742 -N=6672535.414 -E=385351.742 -N=6672342.414 -E=385408.742 -N=6672337.414 -E=385248.242 > L4133B3-filtered.obj

import argparse
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('-N','--north',type=float, action='append')
parser.add_argument('-E','--east',type=float, action='append')
args = parser.parse_args()

es = args.east
ns = args.north

pg = list (zip (es,ns))
polygon = Polygon (pg)

def floats (xs):
  return [float (x) for x in xs]

with open(args.file) as f:
  ls = f.readlines()
ts = [floats (line.split ()) for line in ls]

valid_ts = [x for x in ts if len (x) == 3]
inside = [(e,n,a) for e,n,a in valid_ts if polygon.contains (Point((e,n)))]

xs = [e for e,n,a in inside]
ys = [n for e,n,a in inside]
zs = [a for e,n,a in inside]

x_min = min (xs)
y_min = min (ys)
z_min = min (zs)

for e,n,a in inside:
  x = e - x_min
  y = n - y_min
  z = a
  print (f"v {x:.2f} {y:.2f} {z:.2f}")

