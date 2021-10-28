#!/usr/bin/python

# python cairo-test-strs.py

# ffmpeg -y -framerate 30 -i frames/frame-%06d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p pi-anim-1.mp4

import cairo
from math import *
import os
import shutil

dirpath = "frames"
if os.path.exists (dirpath) and os.path.isdir (dirpath):
  shutil.rmtree (dirpath)

os.mkdir (dirpath)

"""
pi_cent = (
"3.1415926535 8979323846 2643383279 5028841971 6939937510"
"  5820974944 5923078164 0628620899 8628034825 3421170679"
tau_cent = (
"6.2831853071 7958647692 5286766559 0057683943 3879875021" 
"  1641949889 1846156328 1257241799 7256069650 6842341359")
"""

f = open ("pi-digits.txt")
pi_cent = f.read ()
f.close ()

nms = "9876543210."
pi_str = [c for c in pi_cent if c in nms]

w_pic, h_pic = 1280,720
x_margin,y_margin = 20,20
w_img,h_img = w_pic-2*x_margin,h_pic-2*y_margin

fmt = cairo.FORMAT_ARGB32
surface = cairo.ImageSurface(fmt, w_pic, h_pic)
ct = cairo.Context (surface)

def clear ():
  ct.rectangle (0, 0, w_pic, h_pic)
  ct.set_source_rgb (0.95, 0.95, 0.95)
  ct.fill ()

def clear_margins ():
  ct.rectangle (0, 0, x_margin, h_pic)
  ct.rectangle (0, 0, w_pic, y_margin)
  ct.rectangle (w_pic-x_margin, 0, w_pic, h_pic)
  ct.rectangle (0, h_pic-y_margin, w_pic, h_pic)
  ct.set_source_rgb (0.95, 0.95, 0.95)
  ct.fill ()

numbers =  [i for i in "9876543210"]

symbols = numbers + ["dot"]

image_paths = [f"set5/{i}.png" for i in symbols]

surfaces = [cairo.ImageSurface.create_from_png (path)
                     for path in image_paths]

enum = enumerate (zip (symbols, surfaces))

ysurf = {symb: (level,surf) for level,(symb,surf) in enum}
ysurf ["."] = nms.index (pi_str[0]),surfaces[10]

block_w,block_h = 128,128
yfac = (h_img - block_h) / 9

def paint_frame (fr):
  clear ()
  result = 0
  for ix,c in enumerate (pi_str):
    x = block_w * ix - 6 * fr + 1150
    if -block_w < x < w_pic:
      if ix > result:
        result = ix
      y,surf = ysurf [c]
      ct.set_source_surface (surf,x,yfac*y+y_margin)
      ct.paint ()
  clear_margins ()
  surface.write_to_png (
    "frames/frame-" + str(fr).zfill(6) + ".png")
  return result

digits = round (150 * pi)
fr = 0
while True:
  digs = paint_frame (fr)
  fr += 1
  if digs > digits + 1:
    break

