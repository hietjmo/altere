
# python mk-obj.py > stellaro.obj

from stars import stars,abbrs,borders
from math import cos,tau,sin,sqrt
import numpy as np

r = 1.0
cons1 = {}

def rad (deg):
  return tau * deg / 360

for cons in stars:
  cons1 [cons] = []
  for ra,dec,mag in stars[cons]:
    theta = rad (ra)
    phi = rad (dec)
    x = r * cos (phi) * cos (theta)
    y = r * cos (phi) * sin (theta)
    z = r * sin (phi)
    cons1 [cons].append ((round(x,4),round(y,4),round(z,4),mag))

for cons in cons1:
  print (f"o {cons}")
  for x,y,z,mag in cons1[cons]:
    print (f"v {x} {y} {z}")
  print ()

print (f"o axis")
x = 0
y = 0
for z in np.arange (-1.15,1.15,0.1):
  print (f"v {x} {y} {z}")


