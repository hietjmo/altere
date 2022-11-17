#!/usr/bin/python

# python insidium.py

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

center_x, center_y = w_pic/2, h_pic/2
circle_r = 250

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

def intersection (pt1,pt2,pt3,pt4):
  " en.wikipedia.org/wiki/Line-line_intersection "
  x1,y1 = pt1
  x2,y2 = pt2
  x3,y3 = pt3
  x4,y4 = pt4
  nx = (x1*y2-y1*x2) * (x3-x4) - (x1-x2) * (x3*y4-y3*x4)
  ny = (x1*y2-y1*x2) * (y3-y4) - (y1-y2) * (x3*y4-y3*x4)
  d  = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)
  parallel = (d == 0)
  if parallel:
    return None
  else:
    x  = nx / d
    y  = ny / d
    return x,y

def draw_circle (x,y,r):
  ct.arc (x,y,r,0,tau)
  ct.stroke ()

def draw_archie_6 (x,y,r):
  ct.set_line_width (20)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,a,b in [(6,6,7)]:
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc_negative (x,y,r,-a,-b)
    ct.stroke ()

def draw_archie (x,y,r):
  ct.set_line_width (20)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:]+[tau])):
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc_negative (x,y,r,-a,-b)
    ct.stroke ()

def down_up_horiz (center_x,center_y,down,up):
  r = 100
  center = center_x,center_y
  pt2 = add (center,polar_xy (r,down))
  ptx2 = intersection (center,pt2,(0,margin),(w_pic,margin))
  pt3 = add (center,polar_xy (r,up))
  ptx3 = intersection (center,pt3,(0,h_pic - margin),(w_pic,h_pic - margin))
  pt4 = add (center,polar_xy (r,0))
  ptx4 = intersection (center,pt4,(w_pic - margin,0),(w_pic- margin,h_pic))
  # ct.set_source_rgb (*fg_nigre)
  # draw_cross (ptx2[0], ptx2[1], 5)
  # draw_cross (ptx3[0], ptx3[1], 5)
  # draw_cross (ptx4[0], ptx4[1], 5)
  # ct.stroke ()
  d2 = dist(center,ptx2)
  d3 = dist(center,ptx3)
  d4 = dist(center,ptx4)
  # print ("down",ptx2,d2)
  # print ("up",ptx3,d3)
  # print ("horiz",ptx4,d4)
  return min (d2,d3,d4)

def draw_down (r):
  down,up = 6,7
  center = center_x,center_y
  ct.set_dash([])
  ct.set_line_width (1)
  ct.set_source_rgb (*colordict[str(down)])
  ct.move_to (*center)
  pt2 = add (center,polar_xy (r,down))
  ptx = intersection (center,pt2,(0,10),(w_pic,10))
  ct.line_to (*pt2)
  ct.stroke ()

def draw_down_up (down,up,r1,r2):
  center = center_x,center_y
  ct.set_dash([])
  ct.set_line_width (1)
  ct.set_source_rgb (*colordict[down[-1]])
  pt1 = add (center,polar_xy (r1,-float(down)))
  pt2 = add (center,polar_xy (r2,-float(down)))
  ct.move_to (*pt1)
  ct.line_to (*pt2)
  pt3 = add (center,polar_xy (r1,-float(up)))
  pt4 = add (center,polar_xy (r2,-float(up)))
  ct.move_to (*pt3)
  ct.line_to (*pt4)
  ct.stroke ()

def draw_archie_62 (down,up,x,y,r,only="1234567890."):
  rbr = 20
  ct.new_path ()
  ct.set_dash ([])
  ct.set_line_width (rbr)
  ranges = list (np.arange (down,up+0.001,0.1*(up-down)))
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:])):
    if str(i) in only:
      a,b = a - rot_zero, b - rot_zero
      ct.set_source_rgb (*colordict[str(i)])
      ct.arc_negative (x,y,r-rbr/2,-a,-b)
      ct.stroke ()

def draw_cross (x,y,tick_r):
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

def draw_ticks (a=0,b=6):
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,a in enumerate (ranges[a:b+1]):
    a = a - rot_zero
    # print (i,a,b)
    draw_tick (center_x,center_y,circle_r-5,circle_r+5,-a)
  ct.stroke ()

def draw_r ():
  ct.set_line_width (2.0)
  ct.set_dash([13.75,8])
  phi = 0.0 - rot_zero
  pt1 = center_x+10, center_y
  pt2 = add ((center_x, center_y), polar_xy (circle_r-10,phi))
  ct.move_to (*pt1)
  ct.line_to (*pt2)
  ct.stroke ()

def draw_r2 (r1,r2):
  ct.set_line_width (2.0)
  ct.set_dash([13.75,8])
  pt1 = center_x + r1, center_y
  pt2 = center_x + r2, center_y
  ct.move_to (*pt1)
  ct.line_to (*pt2)
  ct.stroke ()

def draw_horiz (x1,x2):
  ct.set_line_width (2.0)
  ct.set_dash([14,8])
  ct.move_to (x1,center_y)
  ct.line_to (x2,center_y)
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

def draw_number (x,y,s,y0=None):
  r = 32
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)
  ct.set_source_rgb (*colordict[s])
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


def draw_number_6 (dot=False):
  r = 32
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)
  for i in [6]:
    s = "6." if dot else "6"
    a = i - rot_zero + tau/42
    pt = add ((center_x, center_y), polar_xy (circle_r+76,a))
    x,y = pt[0],pt[1]
    ct.set_source_rgb (*colordict[s[0]])
    ct.rectangle (x-r,y-r,2*r,2*r)
    ct.fill ()
    ct.set_source_rgb (*bg_blanc)
    x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(s)
    x,y = x-width/2-x_bearing, y+height/2
    ct.move_to (x,y)
    ct.show_text (s)
    return x,y

def draw_dot (x0,y0):
  r = 32
  ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (r)
  for i in [6]:
    symb = "."
    a = i - rot_zero + tau/42
    pt = add ((center_x+70, center_y), polar_xy (circle_r+76,a))
    x,y = pt[0],pt[1]
    ct.set_source_rgb (*colordict[symb])
    ct.rectangle (x-r,y-r,2*r,2*r)
    ct.fill ()
    ct.set_source_rgb (*bg_blanc)
    x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents (symb)
    ct.move_to (x-width/2-x_bearing, y0)
    ct.show_text (symb)

def surface_write_to_png (filename,save=True,duration=1.0):
  if save:
    surface.write_to_png (filename)
  print (F"file '{filename}'")
  print (F"duration {duration:.2f}")

def phase_1 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.set_line_width (2.0)
  ct.set_source_rgb (*eb_gris)
  surface_write_to_png ("phases/phase-1.png",duration=1.00)
  ct.select_font_face("EB Garamond", cairo.FONT_SLANT_NORMAL, 
    cairo.FONT_WEIGHT_NORMAL)
  ct.set_font_size (730)
  s = "τ"
  x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(s)
  x,y = center_x,center_y
  ct.move_to (x-width/2-x_bearing, y+height/2)
  ct.show_text (s)
  surface_write_to_png ('phases/tau-0.png',duration=1.00)

def phase_2 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_cross (center_x, center_y, 5)
  draw_cross (center_x + circle_r, center_y, 5)
  draw_r ()
  centered_text (center_x + circle_r/2,center_y-30,"1")
  surface_write_to_png("phases/phase-2.png")

def draw_arc (x,y,r,a,b):
  ct.arc_negative (x,y,r,a,b)
  ct.stroke ()

def phase_3 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_cross (center_x, center_y, 5)
  draw_r ()
  centered_text (center_x + circle_r/2,center_y-30,"1")
  ct.set_dash([])
  # draw_circle (center_x, center_y, circle_r)
  ranges = list (np.arange (0.0,tau,1.0))
  draw_ticks (0,1)
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:]+[tau])):
    ct.new_path ()
    a = a - rot_zero
    draw_arc (center_x, center_y, circle_r,-a,-b)
    draw_ticks (i,i+1)
    a = a - rot_zero + 0.5
    x,y = add ((center_x, center_y), polar_xy (circle_r-30,-a))
    if i < 6:
      centered_text (x,y,str(i+1))
      surface_write_to_png (f"phases/phase-3-{i}.png")
  surface_write_to_png("phases/phase-3-6.png")

def phase_4 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_cross (center_x, center_y, 5)
  draw_r ()
  ct.set_dash([])
  ct.new_path ()
  draw_circle (center_x, center_y, circle_r)
  draw_ticks ()
  ct.set_line_width (20)
  ranges = list (np.arange (0.0,tau,1.0))
  r = circle_r + 20
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:]+[tau])):
    ct.new_path ()
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc_negative (center_x, center_y, circle_r + 20,-a,-b)
    ct.stroke ()
    r = 32
    ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
    ct.set_font_size (r)
    a = a - rot_zero + tau/42
    pt = add ((center_x, center_y), polar_xy (circle_r+76,-a))
    x,y = pt[0],pt[1]
    ct.set_source_rgb (*colordict[str(i)])
    ct.rectangle (x-r,y-r,2*r,2*r)
    ct.fill ()
    ct.set_source_rgb (*bg_blanc)
    x_bearing, y_bearing, width, height, x_advance, y_advance = ct.text_extents(str(i))
    ct.move_to (x-width/2-x_bearing, y+height/2)
    ct.show_text (str(i))
    surface_write_to_png(f"phases/phase-4-{i}.png")


def phase_5 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_cross (center_x, center_y, 5)
  draw_r ()
  ct.set_dash([])
  ct.new_path ()
  draw_circle (center_x, center_y, circle_r)
  draw_ticks ()
  ct.set_line_width (20)
  r = circle_r + 20
  for (i,a,b) in [(6,6,7)]:
    ct.new_path ()
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc_negative (center_x, center_y, circle_r + 20,-a,-b)
    ct.stroke ()
    r = 32
    ct.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, 
        cairo.FONT_WEIGHT_BOLD)
    ct.set_font_size (r)
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
    surface_write_to_png(f"phases/phase-5.png")


def phase_6 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  arc_r = down_up_horiz (center_x,center_y,6,7)
  draw_down_up ("6","7",circle_r + 20,arc_r)
  draw_archie_62 (6,7,center_x, center_y, arc_r)
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_circle (center_x, center_y, circle_r)
  draw_cross (center_x, center_y, 5)
  draw_archie_6 (center_x, center_y, circle_r + 20)
  draw_ticks ()
  draw_r ()
  draw_r2 (circle_r + 35,arc_r-25)
  #x,y = draw_number_6 ()
  #surface_write_to_png(f"phases/phase-6.png")
  x,y = draw_number_6 (dot=True)
  #draw_dot (x,y)
  surface_write_to_png(f"phases/phase-7.png")


def numbers_10 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  for i in range (0,10):
    draw_number (190+i*100,h_pic-90-i*60,str(i))
    surface_write_to_png (F"phases/numbers-{i}.png",duration=0.52)


def phase_8 ():
  global center_x,center_y
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  center_x = circle_r + margin
  arc_r = down_up_horiz (center_x,center_y,6,7)
  draw_down_up ("6","7", circle_r + 20,arc_r)
  draw_archie_62 (6,7,center_x, center_y, arc_r)

  arc_r_62 = down_up_horiz (center_x,center_y,6.2,6.3)
  draw_down_up ("6.2","6.3",arc_r,arc_r_62)
  draw_archie_62 (6.2,6.3,center_x, center_y, arc_r_62)

  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_circle (center_x, center_y, circle_r)
  draw_cross (center_x, center_y, 5)
  draw_archie_6 (center_x, center_y, circle_r + 20)
  draw_ticks ()
  draw_r ()
  draw_r2 (circle_r + 35,arc_r-25)
  draw_r2 (arc_r + 5,1280 - (circle_r + 2*margin + 25))
  x,y = draw_number_6 (dot=True)
  # draw_dot (x,y)
  surface_write_to_png(f"phases/phase-8-1.png")
  draw_number (826,307,"2")
  surface_write_to_png(f"phases/phase-8-2.png")
  draw_number (1225,299,"8")
  surface_write_to_png(f"phases/phase-8-3.png")




def insidium_4 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  draw_up (circle_r + 210)
  draw_down (circle_r + 210)
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  draw_circle (center_x, center_y, circle_r)
  draw_cross (center_x, center_y, 5)
  draw_archie (center_x, center_y, circle_r + 20)
  draw_ticks ()
  draw_r ()
  draw_numbers ()
  draw_archie_62 (6,7,center_x, center_y, circle_r + 200)
  
  
  surface_write_to_png("phases/insidium-4.png")


def phase_9 ():
  global center_x,center_y
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  center_x = -350
  arc_r = down_up_horiz (center_x,center_y,6,7)
  draw_archie_62 (6,7,center_x, center_y, arc_r,only="2")

  arc_r_62 = down_up_horiz (center_x,center_y,6.2,6.3)
  draw_down_up ("6.2","6.3",arc_r,arc_r_62)
  draw_archie_62 (6.2,6.3,center_x, center_y, arc_r_62)

  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)

  draw_horiz (margin,w_pic-margin)
  x,y = draw_number (margin+16,margin+16,"6")
  draw_number (5+64 + margin+16,margin+16,".",y0=y)
  draw_number (100,center_y-40,"2")
  surface_write_to_png(f"phases/phase-9.png")


def phase_10 ():
  global center_x,center_y
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  center_x = -10550
  #arc_r = down_up_horiz (center_x,center_y,6.2,6.3)
  #arc_r = down_up_horiz (center_x,center_y,6,7)
  arc_r = 10700
  draw_archie_62 (6.2,6.3,center_x, center_y, arc_r,only="8")

  arc_r_62 = down_up_horiz (center_x,center_y,6.28,6.29)
  draw_down_up ("6.28","6.29",arc_r,arc_r_62)
  draw_archie_62 (6.28,6.29,center_x, center_y, arc_r_62)

  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)

  draw_horiz (margin,w_pic-margin)
  x,y = draw_number (margin+16,margin+16,"6")
  draw_number (5+64 + margin+16,margin+16,".",y0=y)
  draw_number (10+128 + margin+16,margin+16,"2")
  draw_number (80,center_y-40,"8")
  surface_write_to_png(f"phases/phase-10.png")


# print (tau_digits)
crear ("phases")
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)
ct = cairo.Context (surface)

numbers_10 ()
phase_1 ()
phase_2 ()
phase_3 ()
phase_4 ()
phase_5 ()
phase_6 ()
phase_8 ()
#phase_9 ()
#phase_10 ()
# insidium_4 ()

# python insidium-start.py > mylist-start.txt
# cat mylist-start.txt mylist.txt mylist-end.txt > mylist-2.txt
# ffmpeg -y -f concat -i mylist-2.txt -c:v libx264 -pix_fmt yuv420p tau-64.mp4

