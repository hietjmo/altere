
# python mk-obj.py > stellaro.obj

from stars import stars,abbrs,borders
from math import cos,tau,sin,sqrt

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

print (cons1)


