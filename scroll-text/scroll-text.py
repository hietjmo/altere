
# python scroll-text.py scroll-text.py -lnum
# ffmpeg -y -i png/%07d.png -c:v libx264 -r 25 -pix_fmt yuv420p scroll-text.mp4

import os
import shutil
import cairo
import argparse
from collections import defaultdict

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-d", "--destpath", default="png")
  pad ("-s", "--step", type=int, default=3)
  pad ("-wx", "--width", type=int, default=1280)
  pad ("-hy", "--height", type=int, default=720)
  pad ("-sz", "--fontsize", type=int, default=24)
  pad ("-font", "--fontname", default="FreeMono")
  pad ("-lnum","--linenumbers", action="store_true")
  pad ("-cnum","--columnnumbers", action="store_true")
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()
destpath = args.destpath
w_pic, h_pic = args.width,args.height
pink = (1.00, 0.9, 0.9)
orange = (0.996, 0.878, 0.761)
black = (0,0,0)
white = (1,1,1)

if os.path.exists (destpath) and os.path.isdir (destpath):
  shutil.rmtree (destpath)
os.mkdir (destpath)

lnes = []
for filename in args.files:
  f = open (filename)
  lns = f.readlines ()
  f.close ()
  lnes.extend (lns)

lines = defaultdict (lambda: "")
for i,x in enumerate (lnes):
  lines [i+1] = x.strip ("\n")
linew = args.fontsize
step = args.step
longor = len (lines)
max_y = linew * longor
lnspc = len (str (longor))
screenln = h_pic // linew

if args.log:
  print ("lines,max_y,lnspc,screenln:",longor,max_y,lnspc,screenln)

def draw_frame (frame, ystart):
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct = cairo.Context (surface)
  font = args.fontname
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_source_rgb (*orange)
  ct.paint ()
  ct.set_font_size (linew)
  ct.set_source_rgb (0.0, 0.0, 0.0)
  lineno, rem = divmod (ystart, linew)
  for i in range (0,screenln+1):
    ct.move_to (6,linew*(i+1) - rem)
    linea = lineno+i+1
    if args.columnnumbers:
      if linea == -1:
        ct.show_text ("".join (
          [str (j % 10) for j in range(1,100)]))
      if linea == -2:
        ct.show_text ("".join( 
          [str (j // 10) if j % 10 == 0 else " " for j in range(1,100)]))
    if 0 < linea <= longor:
      if args.linenumbers:
        ct.show_text (f"{str(linea).rjust(lnspc)} {lines [linea]}")
      else:
        ct.show_text (f"{lines [linea]}")
  outpic = destpath + "/" + str(frame).zfill (7) + '.png'
  surface.write_to_png (outpic)

ystarts = range (-h_pic,max_y,step)
print ("frames =",len (ystarts))

for fr,ystart in enumerate (ystarts):
  draw_frame (fr,ystart)
  if fr % 1000 == 0:
    print ("fr =", fr)

