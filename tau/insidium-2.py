#!/usr/bin/python

# python insidium.py

import cairo
from math import *
import numpy as np

brun = (0.659,0.518,0.392)
blau_obscur = (0.278,0.337,0.467)
violet = (0.573,0.396,0.722)
blau = (0.169,0.510,0.788)
blau_clar = (0.329,0.675,0.824)
verde_obscur = (0.000,0.659,0.522)
verde_clar = (0.380,0.737,0.427)
jalne = (0.969,0.855,0.392)
orange = (0.980,0.627,0.149)
rubie = (0.882,0.290,0.224)
gris = (0.608,0.608,0.608)
bg_gris = (0.96,0.96,0.96)
bg_blanc = (1.00, 1.00, 1.00)
fg_nigre = (0.00, 0.00, 0.00)

colores = [
  ("0",gris),("1",rubie),("2",orange),("3",jalne),
  ("4",verde_clar),("5",verde_obscur),("6",blau_clar),
  ("7",blau),("8",violet),("9",blau_obscur),(".",brun)]
colordict = dict (colores)

numbers =  [i for i in "0123456789"]
symbols = numbers + ["dot"]
image_paths = [f"set5/{i}.png" for i in symbols]
surfaces = [cairo.ImageSurface.create_from_png (path)
                     for path in image_paths]
enum = enumerate (zip (symbols, surfaces))

# rot_zero = 0.25 * tau
rot_zero = 0

w_pic, h_pic = 1280,720
x_margin,y_margin = 20,20
w_img,h_img = w_pic-2*x_margin,h_pic-2*y_margin

center_x, center_y = w_pic/2, h_pic/2
circle_r = 250

def polar_xy (r, phi):
  x = r * cos (phi)
  y = r * sin (phi)
  return (x, y)

def draw_circle (x,y,r):
  ct.arc (x,y,r,0,tau)
  ct.stroke ()

def draw_archie (x,y,r):
  ct.set_line_width (20)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,(a,b) in enumerate  (zip (ranges[0:],ranges[1:]+[tau])):
    a,b = a - rot_zero, b - rot_zero
    # print (i,a,b)
    ct.set_source_rgb (*colordict[str(i)])
    ct.arc (x,y,r,a,b)
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

def draw_ticks ():
  ct.set_line_width (2.0)
  ct.set_source_rgb (*fg_nigre)
  ranges = list (np.arange (0.0,tau,1.0))
  for i,a in enumerate (ranges):
    a = a - rot_zero
    # print (i,a,b)
    draw_tick (center_x,center_y,circle_r-5,circle_r+5,a)
  ct.stroke ()

def draw_r ():
  ct.set_dash([0.0,9.3,15.2,0.0])
  phi = 0.0 - rot_zero
  pt1 = center_x, center_y
  pt2 = add ((center_x, center_y), polar_xy (circle_r,phi))
  ct.move_to (*pt1)
  ct.line_to (*pt2)
  ct.stroke ()

def draw_numbers ():
  ranges = list (np.arange (0.0,tau,1.0))
  for i,a in enumerate (ranges):
    a = a - rot_zero
    # print (i,a,b)
    pt = add ((center_x, center_y), polar_xy (circle_r+76,a))
    pt = add ((-32,-32),pt)
    x,y = pt[0],pt[1]
    # ct.save ()
    ct.set_source_surface (surfaces[i],*pt)
    pattern = ct.get_source ()
    scalematrix = cairo.Matrix ()
    scalematrix.scale (2,2)
    scalematrix.translate (-x,-y)
    pattern.set_matrix(scalematrix)  
    ct.paint ()
    # ct.restore ()

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)

ct = cairo.Context (surface)

ct.rectangle (0, 0, w_pic, h_pic)
ct.set_source_rgb (*bg_gris)
ct.fill()

ct.set_line_width (2.0)
ct.set_source_rgb (*fg_nigre)
draw_circle (center_x, center_y, circle_r)
draw_cross (center_x, center_y, 5)
draw_archie (center_x, center_y, circle_r + 20)
draw_ticks ()
draw_r ()
draw_numbers ()

surface.write_to_png("insidium-2.png")

