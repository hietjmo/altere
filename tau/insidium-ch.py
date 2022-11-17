#!/usr/bin/python

# python insidium-ch.py

import os
import shutil
import cairo
from math import *
import numpy as np

tau_digits = ''.join(c for c in ("""
6.
2831853071 7958647692 5286766559 0057683943 3879875021 
1641949889 1846156328 1257241799 7256069650 6842341359 
6429617302 6564613294 1876892191 0116446345 0718816256 
9622349005 6820540387 7042211119 2892458979 0986076392 
8857621951 3318668922 5695129646 7573566330 5424038182 
9129713384 6920697220 9086532964 2678721452 0498282547 
4491740132 1263117634 9763041841 9256585081 8343072873 
5785180720 0226610610 9764093304 2768293903 8830232188 
6611454073 1519183906 1843722347 6386522358 6210237096 
1489247599 2549913470 3771505449 7824558763 6602389825
""") if c in "1234567890.")

brun = (0.659,0.518,0.392)
blau_obscur = (0.278,0.337,0.467)
violet = (0.573,0.396,0.722)
blau = (0.169,0.510,0.788)
#blau_clar = (0.329,0.675,0.824)
blau_clar = (0.660,0.888,0.937)
verde_obscur = (0.000,0.659,0.522)
#verde_clar = (0.380,0.737,0.427)
verde_clar = (0.525,0.855,0.498)
jalne = (0.969,0.855,0.392)
orange = (0.980,0.627,0.149)
rubie = (0.882,0.290,0.224)
gris = (0.608,0.608,0.608)
eb_gris = (0.337,0.361,0.396)
ch_gris = (0.80,0.80,0.80)
bg_gris = (0.96,0.96,0.96)
bg_blanc = (1.00, 1.00, 1.00)
fg_nigre = (0.00, 0.00, 0.00)

colores = [
  ("0",gris),("1",blau_obscur),("2",violet),("3",blau),
  ("4",blau_clar),("5",verde_obscur),("6",verde_clar),
  ("7",jalne),("8",orange),("9",rubie),(".",brun)]

colordict = dict (colores)

numbers =  [i for i in "0123456789"]
symbols = numbers + ["dot"]

# rot_zero = 0.25 * tau
rot_zero = 0

w_pic, h_pic = 1280,720
margin,x_margin,y_margin = 20,20,20
w_img,h_img = w_pic-2*x_margin,h_pic-2*y_margin
numrect_r = 32

center_x, center_y = w_pic/2, h_pic/2

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)

def polar_xy (r, phi):
  x = r * cos (phi)
  y = r * sin (phi)
  return (x, y)

def dist (pt1,pt2): 
  dx = pt2[0] - pt1[0]
  dy = pt2[1] - pt1[1]
  return sqrt (dx*dx + dy*dy)

def draw_circle (x,y,r):
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  ct.arc (x,y,r,0,tau)
  ct.stroke ()

def draw_cross (x,y,tick_r):
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  ct.move_to (x-tick_r, y)
  ct.line_to (x+tick_r, y)
  ct.move_to (x, y-tick_r)
  ct.line_to (x, y+tick_r)
  ct.stroke ()

def add (pt1,pt2):
  (x1,y1),(x2,y2) = pt1,pt2
  return x1+x2, y1+y2

def draw_tick (x0,y0,r1,r2,phi):
  pt1 = add ((x0,y0), polar_xy (r1,phi))
  pt2 = add ((x0,y0), polar_xy (r2,phi))
  ct.move_to (*pt1)
  ct.line_to (*pt2)

def draw_ticks (center_x,center_y,circle_r):
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  ranges = list (np.arange (0.0,-tau,-1.0))
  for i,a in enumerate (ranges):
    a = a - rot_zero
    # print (i,a,b)
    draw_tick (center_x,center_y,circle_r-5,circle_r+5,a)
  ct.stroke ()

def centered_text (x,y,s):
  r = 32
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)

  x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(s)
  ct.move_to (x-width/2-x_bearing, y+height/2)
  ct.show_text (s)

def draw_numbers ():
  r = 32
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,a in enumerate (ranges):
    a = a - rot_zero + tau/42
    pt = add ((center_x, center_y), polar_xy (circle_r+76,a))
    x,y = pt[0],pt[1]
    ct.set_source_rgb (*colordict[str(i)])
    ct.rectangle (x-r,y-r,2*r,2*r)
    ct.fill ()
    ct.set_source_rgb (*bg_blanc)
    x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(str(i))
    ct.move_to (x-width/2-x_bearing, y+height/2)
    ct.show_text (str(i))

def draw_number (x,y,s,r=29,y0=None):
  ct.set_source_rgb (*bg_gris)
  ct.rectangle (x-r,y-r,2*r,2*r)
  ct.fill ()
  r = r - 1
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)
  ct.set_source_rgb (*colordict[s[0]])
  ct.rectangle (x-r,y-r,2*r,2*r)
  ct.fill ()
  ct.set_source_rgb (*bg_blanc)
  x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(s)
  x1,y1 = x-width/2-x_bearing, y+height/2
  if y0:
    y1 = y0
  ct.move_to (x1,y1)
  ct.show_text (s)
  return x1,y1

def draw_trigs (x1,x2):
  r1,r2 = 20,6
  ct.set_source_rgb (*fg_nigre)
  ct.move_to (x1,center_y)
  ct.line_to (x1-r1,center_y-r2)
  ct.line_to (x1-r1,center_y+r2)
  ct.close_path ()
  ct.move_to (x2,center_y)
  ct.line_to (x2+r1,center_y-r2)
  ct.line_to (x2+r1,center_y+r2)
  ct.close_path ()
  ct.fill ()

def rainbow (x0,y0,x1,y1):
  down,up=0,1
  ranges = list (np.arange (down,up+0.001,0.1*(up-down)))
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:])):
    ct.set_source_rgb (*colordict[str(i)])
    x2,y2 = x0,y0+a*(y1-y0)
    x3,y3 = x1,y0+b*(y1-y0)
    if y3 <= h_pic and y2 >= 0.0:
      y2 = min (h_pic,y2)
      y3 = max (0.0,y3)
      ct.move_to (x2,y2)
      ct.line_to (x3,y2)
      ct.line_to (x3,y3)
      ct.line_to (x2,y3)
      ct.close_path ()
      ct.fill ()

def rect (x0,y0,w1,h1):
  x1,y1 = x0,y0
  x2,y2 = x0+w1,y0+h1
  y1 = min (h_pic,y1)
  y2 = min (h_pic,y2)
  ct.move_to (x1,y1)
  ct.line_to (x2,y1)
  ct.line_to (x2,y2)
  ct.line_to (x1,y2)
  ct.close_path ()
  ct.fill ()

def rect1 (x1,y1,x2,y2):
  ct.move_to (x1,y1)
  ct.line_to (x2,y1)
  ct.line_to (x2,y2)
  ct.line_to (x1,y2)
  ct.close_path ()
  ct.fill ()

def draw_square (x,y,r=29,y0=None):
  ct.rectangle (x-r,y-r,2*r,2*r)
  ct.fill ()

def draw_chess_board ():
  ct.set_source_rgb (*eb_gris)
  ct.rectangle (20,118,484,484)
  ct.fill ()
  for x in range (0,8):
    for y in range (0,8):
      light = (x % 2) == (y % 2)
      if light:
        ct.set_source_rgb (*ch_gris)
      else:
        ct.set_source_rgb (*eb_gris)
      x1,y1=59+58*x,157+58*y
      draw_square (x1,y1)

def draw_decimals (m):
  draw_chess_board ()
  if len (tau_digits) > m:
    for n in range (0,m):
      s = tau_digits [n+1]
      x,y=59+58*(n%8),157+58*(n//8)
      if n == 0:
        draw_number (x,y,"6.",r=29)
      else:
        x0,y0 = draw_number (x,y,s,r=29)

def draw_r (center_x,center_y,r1,r2):
  offset = (r2-r1) % 10
  ct.set_line_width (2.0)
  ct.set_dash ([10,5],offset)
  ct.set_source_rgb (*fg_nigre)

  pt1 = center_x + r1, center_y
  pt2 = center_x + r2, center_y
  ct.move_to (*pt1)
  ct.line_to (*pt2)
  ct.stroke ()
  ct.set_dash([])

def draw_archie (x,y,r,lw):
  ct.set_line_width (lw)
  ranges = list (np.arange (0.0,tau,1.0))
  # ranges = list (np.arange (0.0,11.0,1.0))
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:]+[tau])):
  # for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:])):
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc_negative (x,y,r,-a,-b)
    ct.stroke ()

def draw_frames (start=0,end=5400):
  cx,cy = center_x,center_y
  x0 = cx + 40
  f = open ("mylist.txt","w")
  ct.set_line_width (2)
  ct.new_path ()
  tau_desi = "0.6" + tau_digits [2:]
  rbw = 20
  trigs1,trigs2 = 60,100
  for ik in range (start,end):
    i = 0.36 * ik # 0.9 × 
    if ik % 100 == 0:
      print ("frame =",i)
    ct.new_path ()
    ct.set_source_rgb (*bg_gris)
    ct.paint ()
    decs,ones = divmod (i,9)
    m = 10**decs
    n = (ones+1) * m
    condensed = 20*(decs+3) >= center_x
    if condensed:
      superflue = 20*(decs+3) - center_x 
      x0 = max (20,center_x - superflue)
      rbw = (w_pic - x0 - 20) / (decs+1)
      cx = x0 - 40
    condensed2 = rbw < 20
    trigs1,trigs2 = x0,x0+rbw*(decs+1)
    draw_trigs (trigs1,trigs2)
    for ii in range (0,int(decs+1)):
      s = tau_desi [ii+2:ii+17]
      p1 = float ("0." + s)
      p2 = 1.0 - p1
      j = i % 9 + 1
      rr = 10**(decs-ii) * j
      rr = 120*rr
      p1 = rr * p1
      p2 = rr * p2
      r = p1 / tau
      if ii == 0 and not condensed2:
        r = min (5_000_000+3*i,r+4*i)
        draw_circle (cx-r, cy, r)
        draw_archie (cx-r, cy, r+10,4)
        if r > 20:
          draw_r (cx-r, cy, 7, r-7)
        draw_cross (cx-r, cy, 5)
        if r > 30:
          draw_ticks (cx-r, cy, r)
      if p1 < 999999 and p2 < 999999:
        rainbow (x0+rbw*ii, cy+p1, x0+rbw*(ii+1), cy-p2)
      else:
        ct.set_source_rgb (*colordict[s[0]])
        rect1 (x0+rbw*ii,0,x0+rbw*(ii+1),h_pic)
    draw_decimals (ii+1)
    filename = f"pics/frame-{ik}.png"
    f.write (F"file '{filename}'\n")
    f.write ("duration 0.04\n")
    surface.write_to_png (filename)
  f.write (F"file '{filename}'\n")

# print (tau_digits)
crear ("pics")
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)
ct = cairo.Context (surface)

# draw_phases (1935)
# draw_phases (5400)
draw_frames (0,1600)

# python insidium-ch.py
# ffmpeg -y -f concat -i mylist.txt -c:v libx264 -pix_fmt yuv420p tau-001.mp4

