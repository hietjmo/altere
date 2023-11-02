
from stars import stars
from math import cos,tau,sin,sqrt,atan,asin,atan2
import os
import shutil
import cairo
import random
import numpy as np
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-wx", "--width", type=int, default=610)
  pad ("-hy", "--height", type=int, default=610)
  pad ("-lon","--center_lon",type=float,default=180.0) 
  pad ("-lat","--center_lat",type=float,default=90.0)
  pad ("-seed",type=int)
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

if args.seed:
  random.seed (args.seed)

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)

path = "png"
crear (path)

def from_hex (h):
  return tuple (round (int(h.lstrip('#')[i:i+2], 16)/255,2) for i in (0,2,4))

p1 = [ "#fbb4ae", "#b3cde3", "#ccebc5", "#decbe4", "#fed9a6", 
       "#ffffcc", "#e5d8bd", "#fddaec", "#f2f2f2", ]

palette1 = [from_hex (h) for h in p1]

width, height = args.width, args.height
r_spe = (min (width, height) -10)/2
center_lon, center_lat = args.center_lon, args.center_lat

def rad (th):
  return th / 360 * tau

def deg (th):
  return th / tau * 360

def orthographic (theta,phi,theta1,phi1,R):
  theta = rad (theta)
  phi = rad (phi)
  theta1 = rad (theta1)
  phi1 = rad (phi1)
  x = R * cos (phi) * sin (theta - theta1)
  y = R * (cos (phi1) * sin (phi) - sin (phi1) * cos (phi) * cos (theta - theta1))
  cosc = sin (phi1) * sin (phi) + cos (phi1) * cos (phi) * cos (theta - theta1)
  return (x,y,cosc)

def inverse_orthographic (x,y,phi1,theta1,R):
  phi1 = rad (phi1)
  theta1 = rad (theta1)
  rho = sqrt (x**2 + y**2)
  c = asin (rho/R)
  phi = asin (cos(c)*sin(phi1) + (y*sin(c)*cos(phi1)/rho))
  theta = theta1 + atan ((x*sin(c))/(rho*cos(c)*cos(phi1)-y*sin(c)*sin(phi1)))
  return (theta,phi)

def polygon (ct,pts):
  ct.move_to (*pts[0])
  for pt in pts [1:]:
    ct.line_to (*pt)
  ct.close_path()

def paint_star (ct,ra,dec,mag,center_lon,center_lat):
  rho = 0.525731
  R = 0.200811
  r1 = 15-1.25*mag
  star_points = []
  pegs = 10
  rnd = random.random()
  for t in range (pegs):
    rh = rnd * (2/pegs) * tau
    theta = (t/pegs) * tau + rh
    r = rho*r1 if t % 2 == 0 else R*r1
    x1 = r * sin (theta)
    y1 = r * -cos (theta)
    z = r_spe
    x,y,cosc = orthographic (ra,dec,center_lon,center_lat,r_spe)
    x,y = x+width/2,y+height/2
    if cosc > 0:
      star_points.append ((x+x1,y+y1))
  if star_points:
    polygon(ct, star_points)
    ct.fill()

def paint_name (ct,name,ra,dec,center_lon,center_lat):
  x,y,cosc = orthographic (ra,dec,center_lon,center_lat,r_spe)
  x1,y1 = x+width/2,y+height/2
  xbear, ybear, wt, ht, xadv, yadv = ct.text_extents (name)
  if cosc > 0:
    ct.move_to (x1-wt/2,y1+ht/3)
    ct.show_text (name)

colors = {}
for cons in stars:
  colors[cons] = random.choice (palette1)

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ct = cairo.Context(surface)

i = 0
delta_lat = 0
# for delta_lat in np.arange (0,360,0.25):
if True:
  i = i + 1
  ct.set_source_rgb (1.00, 1.00, 1.00)
  ct.paint ()
  pattern = cairo.RadialGradient (height/2,width/2,150,height/2,width/2,300)
  pattern.add_color_stop_rgb (1,1,1,1)
  pattern.add_color_stop_rgb (0,0,0,0)
  ct.set_source (pattern)
  ct.mask (pattern)
  ct.set_source_rgb (0.99, 1.00, 0.85)
  names = []
  for cons in stars:
    ras,decs = [],[]
    for ra,dec,mag in stars[cons]:
      ct.set_source_rgb (*colors[cons])
      ras.append (ra)
      decs.append (dec) 
      paint_star (ct,ra,dec,mag,center_lon+delta_lat,center_lat+delta_lat)
    dec1 = sum (decs) / len (decs)
    ra1 = sum (ras) / len (ras)
    names.append ((cons,ra1,dec1))
    paint_name (ct,cons,ra1,dec1,center_lon+delta_lat,center_lat+delta_lat)
  surface.write_to_png (f"png/star-image{i:05}.png")

