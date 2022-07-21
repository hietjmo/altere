
import os
import shutil
import cairo
import argparse
from collections import defaultdict
from subprocess import run,DEVNULL,STDOUT

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-d1", "--destpath1", default="png")
  pad ("-d2", "--destpath2", default="wav")
  pad ("-d3", "--destpath3", default="mp4")
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
w_pic, h_pic = args.width,args.height
pink = (1.00, 0.9, 0.9)
orange = (0.996, 0.878, 0.761)
green = (0.220, 0.780, 0.278)
purple = (0.561, 0.220, 0.780)
yellow = (0.988,0.918,0.169)
blue = 0.22, 0.44, 0.78
red = 0.83, 0.00, 0.00
black = (0,0,0)
white = (1,1,1)

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)

for p in [args.destpath1,args.destpath2,args.destpath3]:
  crear (p)

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
max_y = linew * longor + 2*step
lnspc = len (str (longor))
screenln = h_pic // linew
mid = screenln // 2

def draw_linea (lineno,outpic):
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct = cairo.Context (surface)
  font = args.fontname
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_source_rgb (*orange)
  ct.paint ()
  ct.set_font_size (linew)
  ct.set_source_rgb (0.0, 0.0, 0.0)
  rem = 0
  for i in range (0,screenln+1):
    ct.move_to (6,linew*(i+1) - rem)
    linea = lineno+i+1 - mid
    if linea == lineno:
      ct.set_source_rgb (*red)
    else:
      ct.set_source_rgb (*black)
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
  surface.write_to_png (outpic)

f = open ("mylist.txt","w")
for i in range(1,longor+1):
  outpic = args.destpath1 + "/" + str(i).zfill (7) + '.png'
  draw_linea (i,outpic)
  print (lines[i])
  outwav = args.destpath2 + "/" + str(i).zfill (7) + '.wav'
  run(["espeak", lines[i], "-w", outwav])
  outmp4 = args.destpath3 + "/" + str(i).zfill (7) + '.mp4'
  run(["/usr/bin/ffmpeg", "-y", "-i", f"{outpic}", "-i", 
    f"{outwav}", "-acodec", "aac", "-vcodec", "libx264", 
    "-pix_fmt", "yuv420p", f"{outmp4}"],
    stdout=DEVNULL, stderr=STDOUT
  )
  f.write (f"file '{outmp4}'\n")
f.close ()

print ("ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy output.mp4")
run(["/usr/bin/ffmpeg", "-y", "-f", "concat", "-safe", "0", 
  "-i", "mylist.txt", "-c", "copy", "output.mp4"],
  stdout=DEVNULL, stderr=STDOUT
)

