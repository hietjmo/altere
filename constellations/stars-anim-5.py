
from stars import stars,abbrs,borders
from finnish import finnish
from math import cos,tau,sin,sqrt
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
  pad ("-wx", "--width", type=int, default=640)
  pad ("-hy", "--height", type=int, default=640)
  pad ("-grid", action="store_true")
  pad ('-l','--list', nargs='*')
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
pngs = []
frame = 0

ccolors = {'Ser': 'grey', 'Hya': 'red', 'Sgr': 'blue', 'Eri': 'green', 'Leo': 'violet', 'Her': 'orange', 'Cen': 'yellow', 'Aqr': 'brown', 'Aql': 'pink', 'Vir': 'blue', 'UMa': 'red', 'Pup': 'green', 'Peg': 'violet', 'Hyi': 'orange', 'Dra': 'yellow', 'Cam': 'brown', 'Boo': 'pink', 'Tau': 'red', 'Sco': 'green', 'Per': 'blue', 'Oph': 'violet', 'Oct': 'yellow', 'Mon': 'orange', 'Lyn': 'pink', 'Lib': 'brown', 'Ind': 'grey', 'Gem': 'blue', 'Dor': 'red', 'Cet': 'violet', 'Car': 'orange', 'Ara': 'yellow', 'Aps': 'green', 'Vul': 'brown', 'Tuc': 'pink', 'Tel': 'red', 'Scl': 'grey', 'Psc': 'blue', 'Pic': 'violet', 'Phe': 'yellow', 'Mus': 'brown', 'Mic': 'green', 'Lup': 'orange', 'Lep': 'pink', 'Gru': 'red', 'Del': 'grey', 'Cyg': 'blue', 'Cnc': 'green', 'Cir': 'violet', 'Cha': 'pink', 'Cep': 'orange', 'Cae': 'yellow', 'And': 'brown', 'Vol': 'grey', 'Vel': 'red', 'PsA': 'blue', 'Pav': 'violet', 'Ori': 'yellow', 'Nor': 'brown', 'Men': 'green', 'Lac': 'pink', 'Hor': 'grey', 'Crt': 'orange', 'Com': 'green', 'Col': 'red', 'Cas': 'violet', 'Cap': 'orange', 'Aur': 'yellow', 'Ari': 'brown', 'Tri': 'pink', 'TrA': 'blue', 'Sge': 'red', 'Pyx': 'grey', 'Lyr': 'green', 'LMi': 'blue', 'For': 'orange', 'CrA': 'violet', 'CMi': 'yellow', 'CMa': 'brown', 'Ant': 'pink', 'UMi': 'grey', 'Sex': 'blue', 'Sct': 'red', 'Ret': 'green', 'Equ': 'orange', 'CVn': 'violet', 'Crv': 'yellow', 'CrB': 'brown', 'Cru': 'pink'}



def from_hex (h):
  return tuple (round (int(h.lstrip('#')[i:i+2], 16)/255,2) for i in (0,2,4))

p1 = [ "#fbb4ae", "#b3cde3", "#ccebc5", "#decbe4", "#fed9a6", 
       "#ffffcc", "#e5d8bd", "#fddaec", "#f2f2f2", ]
p2 = ['red', 'blue', 'green', 'violet', 'orange', 'yellow', 'brown', 'pink', 'grey']
palette1 = [from_hex (h) for h in p1]
palette3 = dict (zip(p2,palette1))

width, height = args.width, args.height
r_spe = (min (width, height) -10)/2


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

def polygon (ct,pts,numbered=False):
  if numbered:
    for i,pt in enumerate (pts):
      ct.move_to (*pt)
      ct.show_text (str(i))
      print (i,pt)
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
  # rnd = random.random()
  rnd = ra+100*center_lon/360 + dec+100*(center_lat+90)/180
  for t in range (pegs):
    rh = rnd * (2/pegs) * tau
    theta = (t/pegs) * tau + rh
    r = rho*r1 if t % 2 == 0 else R*r1
    x1 = r * sin (theta)
    y1 = r * -cos (theta)
    z = r_spe
    x,y,cosc = orthographic (ra,dec,center_lon,center_lat,r_spe)
    x,y = width/2-x,height/2-y
    if cosc > 0:
      star_points.append ((x+x1,y+y1))
  if star_points:
    polygon(ct, star_points)
    ct.fill()

def paint_name (ct,name,ra,dec,center_lon,center_lat):
  x,y,cosc = orthographic (ra,dec,center_lon,center_lat,r_spe)
  x1,y1 = width/2-x,height/2-y
  xbear, ybear, wt, ht, xadv, yadv = ct.text_extents (name)
  if cosc > 0:
    ct.move_to (x1-wt/2,y1+ht/3)
    ct.show_text (name)

colors = {}
for cons in stars:
  colors[cons] = random.choice (palette1)

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ct = cairo.Context(surface)

def dist (a,b):
  lat0,lon0 = a
  lat1,lon1 = b
  dy = lat1 - lat0
  dx = lon1 - lon0
  return sqrt (dx*dx + dy*dy)

def diff (a,b):
  lat0,lon0 = a
  lat1,lon1 = b
  dy = lat1 - lat0
  dx = lon1 - lon0
  return dy,dx

def easeInOut (t):
  if t > 0.5: 
    result = 4*((t-1)**3)+1 
  else: 
    result = 4*(t**3);
  return result

for cons in stars:
  ras,decs,mags = [],[],[]
  for ra,dec,mag in stars[cons]:
    ras.append (ra)
    decs.append (dec)
    mags.append (mag)
  ras2 = ras.copy()
  if max (ras) - min (ras) > 330:
    ras2 = []
    for r in ras:
      if r < 50:
        ras2.append (r+360)
      else:
        ras2.append (r)
  stars [cons] = [(ra,dec,mag) for ra,dec,mag in zip (ras2,decs,mags)]

def paint_grid (ct,center_lon,center_lat):
  ct.set_line_width(0.5)
  # Parallels (incl. equator):
  rng = list (range (0,365,5))
  for lat in range (-90,95,15):
    pg = []
    for lon1,lon2 in zip (rng,rng[1:]):
      if lat == 0:
        ct.set_source_rgb (0.74,0.40,0.87)
      elif lat > 0:
        ct.set_source_rgb (0.74,0.89,0.97)
      else:
        ct.set_source_rgb (0.99,0.50,0.50)
        
      x1,y1,cosc1 = orthographic (lon1,lat,center_lon,center_lat,r_spe)
      x1,y1 = width/2-x1,height/2-y1
      x2,y2,cosc2 = orthographic (lon2,lat,center_lon,center_lat,r_spe)
      x2,y2 = width/2-x2,height/2-y2

      if cosc1 > 0 and cosc2 > 0:
        ct.move_to (x1,y1)
        ct.line_to (x2,y2)
        ct.stroke ()
  # Meridians:
  rng = list (range (-90,95,5))
  for lon in range (0,359,30):
    pg = []
    for lat1,lat2 in zip (rng,rng[1:]):
      if lon == 0:
        ct.set_source_rgb (0.60,0.90,0.60)
      elif lat2 > 0:
        ct.set_source_rgb (0.74,0.89,0.97)
      else:
        ct.set_source_rgb(0.99,0.50,0.50)

      x1,y1,cosc1 = orthographic (lon,lat1,center_lon,center_lat,r_spe)
      x1,y1 = width/2-x1,height/2-y1
      x2,y2,cosc2 = orthographic (lon,lat2,center_lon,center_lat,r_spe)
      x2,y2 = width/2-x2,height/2-y2

      if cosc1 > 0 and cosc2 > 0:
        ct.move_to (x1,y1)
        ct.line_to (x2,y2)
        ct.stroke ()

# borders3 = {"UMi": [borders ["UMi"][0][15:17]]}
borders2 = {}
for abbr in borders:
  borders2[abbr] = []
  for pg1 in borders[abbr]:
    pg2 = []
    for (ra3,dec3),(ra4,dec4) in zip(pg1,pg1[1:]+[pg1[0]]):
      ra5 = ra3
      ra6 = ra4
      route1 = abs (ra4-ra3)
      route2 = abs (360-ra3) + ra4
      route3 = ra3 + abs (360-ra4)
      # 339, 135
      if route2 < route1:
        ra6 = ra4 + 360.0
      if route3 < min (route1,route2):
        ra5 = ra3 + 360.0
      division = 0.3 * abs (ra6-ra5)
      for i in np.arange(0.0,1.0,1/division):
        pg2.append ((ra5+i*(ra6-ra5),dec3+i*(dec4-dec3)))
    borders2[abbr].append (pg2)

def paint (ct,center_lon,center_lat,abbr,stable=False):
  ct.set_source_rgb (1.00, 1.00, 1.00)
  ct.set_line_width (2.0)
  ct.paint ()
  pattern = cairo.RadialGradient (height/2,width/2,(width-10)/4,height/2,width/2,(width-10)/2)
  pattern.add_color_stop_rgb (1,1,1,1)
  pattern.add_color_stop_rgb (0,0.08,0.13,0.20)
  ct.set_source (pattern)
  ct.paint ()
  if abbr in borders2:
    ct.set_source_rgb (0.70,0.30,0.30)
    for pg1 in borders2[abbr]:
      pg2 = []
      for ra3,dec3 in pg1:
        x,y,cosc = orthographic (ra3,dec3,center_lon,center_lat,r_spe)
        x,y = width/2-x,height/2-y
        pg2.append ((x,y))
      # polygon (ct,pg2,numbered=True)
      polygon (ct,pg2)
    ct.stroke ()
  names = []
  for cons in stars:
    ras,decs = [],[]
    for ra,dec,mag in stars[cons]:
      ct.set_source_rgb (*palette3[ccolors[cons]])
      ras.append (ra)
      decs.append (dec) 
      paint_star (ct,ra,dec,mag,center_lon,center_lat)
    dec1 = sum (decs) / len (decs)
    ra1 = sum (ras) / len (ras)
    names.append ((cons,ra1,dec1))
    paint_name (ct,abbrs[cons],ra1,dec1,center_lon,center_lat)
  ct.set_source_rgb (0.00, 0.00, 0.00)
  if abbr in abbrs:
    ct.move_to (7,15)
    ct.show_text (f"{abbrs[abbr]} ({finnish[abbr]})")
    print (abbrs[abbr])
  if args.grid:
    paint_grid (ct,center_lon,center_lat)
  pngfile=f"png/rot_{center_lon:.3f}_{center_lat:.3f}{'S' if stable else 'T'}.png"
  surface.write_to_png (pngfile)
  if stable:
    for i in range (0,30):
      pngs.append (pngfile)
  else:
    pngs.append (pngfile)

def transit (ct,lon0,lat0,lon1,lat1):
  a = (lat0,lon0)
  b = (lat1,lon1)
  dy,dx = diff (a,b)
  print ("dy,dx: ", dy,dx)
  d = dist (a,b)
  frames = d // 8
  frames = max (4,frames)
  print ("frames:",frames)
  step = 1.0/frames
  for g in np.arange(0.0, 1.0+step, step):
    g1 = easeInOut (g)
    lat2 = lat0 + g1 * dy 
    lon2 = lon0 + g1 * dx
    paint (ct,lon2,lat2,"",stable=False)

def paint_stable (ct,start,center_lon,center_lat):
  paint (ct,center_lon,center_lat,start,stable=True)

lst = ['Ari', 'Tau', 'Gem', 'Cnc', 'Leo', 'Vir', 'Lib', 'Sco', 'Sgr', 'Cap', 'Aqr', 'Psc', 'UMi', 'UMa', 'Dra', 'Cep', 'Boo', 'CrB', 'Her', 'Lyr', 'Cyg', 'Cas', 'Per', 'Aur', 'Oph', 'Ser', 'Sge', 'Aql', 'Del', 'Equ', 'Peg', 'And', 'Tri', 'Cet', 'Ori', 'Eri', 'Lep', 'CMa', 'CMi', 'Hya', 'Crt', 'Crv', 'Cen', 'Lup', 'Ara', 'CrA', 'PsA', 'Cam', 'Com', 'Mon', 'Cha', 'Gru', 'Tuc', 'Aps', 'Mus', 'Pav', 'Cru', 'Col', 'Dor', 'Hyi', 'Ind', 'Phe', 'TrA', 'Vol', 'Lyn', 'LMi', 'CVn', 'Vul', 'Lac', 'Sct', 'Sex', 'Men', 'Hor', 'Pic', 'Ret', 'Cir', 'Nor', 'Scl', 'Car', 'Pup', 'Vel', 'Tel', 'Pyx', 'Oct', 'Mic', 'For', 'Cae', 'Ant']

lst = [lst[-1]] + lst
if args.list:
  lst = args.list
for start,end in list (zip (lst,lst[1:])):
  print (start,end)
  ras,decs = [],[]
  for ra,dec,mag in stars[start]:
    ras.append (ra)
    decs.append (dec) 
  dec1 = sum (decs) / len (decs)
  ra1 = sum (ras) / len (ras)
  ras,decs = [],[]
  for ra,dec,mag in stars[end]:
    ras.append (ra)
    decs.append (dec) 
  dec2 = sum (decs) / len (decs)
  ra2 = sum (ras) / len (ras)
  transit (ct,ra1,dec1,ra2,dec2)
  paint_stable (ct,end,ra2,dec2)

with open("mylist.txt","w") as f:
 for p in pngs:
  f.write (f"file '{p}'\nduration 0.1\n")
 f.write (f"file '{p}'\n") 

"""
ffmpeg -y -r 20 -f concat -i mylist.txt -c:v libx264 -pix_fmt yuv420p out.mp4

Oct': [[[0.8006, -89.3039], [1.5334, -81.804], [50.0917, -82.0645], [48.2329, -84.5554], [109.0197, -85.2614],
 [111.6521, -82.7759], [209.1111, -83.1201], [276.866, -82.4583], [274.1951, -74.9745], [323.1848, -74.4545],
 [351.9978, -74.3125], [1.5663, -74.304], [0.8006, -89.3039], [0.8007, -89.3039]]]

"""
