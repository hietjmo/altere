
# python suuret-numerot-tau.py -i 45

import cairo
from numeraalit import numeraali
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ("-n", "--number", type=int, default=0)
  parser.add_argument ("-i", "--items", type=int, default=0)
  args = parser.parse_args ()
  return (args)

args = read_args()


f = open ("tau-digits.txt")
txt = f.read ()
f.close ()

nms = "1234567890."
tau_list = [c for c in txt if c in nms]

t = []
s = ""
for c in tau_list:
  if s == "" and c == "0" and "0" in t:
    t[-1] = t [-1] + c
    continue
  s = s + c
  if s not in t:
    t.append (s)
    s = ""
  if args.number and i > args.number:
    break
  if args.items and len (t) > args.items:
    break

def create_surface (filename,w_pic,h_pic,bg):
  if filename.endswith (".png"):
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  if filename.endswith (".pdf"):
    surface = cairo.PDFSurface (filename, w_pic, h_pic)
  ct = cairo.Context (surface)
  ct.set_source_rgb (*bg)
  ct.paint ()
  return ct,surface

outpic = ".png"
pink = (1.00, 0.9, 0.9)
orange = (0.996, 0.878, 0.761)
fgcolor = (0.85, 0.45, 0.45)
black = (0,0,0)
white = (1,1,1)

def generator1 (numtext):
  while True:
    for c in numtext:
      yield c

def chunks (lst, n):
  """Yield successive n-sized chunks from lst."""
  for i in range (0, len (lst), n):
    yield lst [i:i + n]

def paint_pic (instr,outpic):

  # 1280x960
  font = "DejaVu Serif"
  ct,surface = create_surface (outpic,1280,720,white)
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (750)
  (x, y, w, h, dx, dy) = ct.text_extents (instr)
  ct,surface = create_surface (outpic,int(dx),720,white)
  ct.select_font_face(font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (750)
  ct.set_source_rgb (*black)
  ct.move_to (0, 645)
  ct.show_text (instr)
  
  font = "FreeMono"
  
  if instr == ".":
    numstr = "piste"
  else:
    numero = int (instr)
    text = str (numero)
    numstr = numeraali (numero)
  
  numtext = numstr + "·"
  
  outpic = 'pics/numero-' + numstr + '.png'
  
  
  
  surface1 = surface
  pic_w, pic_h = surface1.get_width (), surface1.get_height ()
  
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, pic_w, pic_h)
  ct = cairo.Context (surface)
  ct.set_source_rgb (*orange)
  ct.paint ()
  
  pixel_data_mv = surface1.get_data ()
  pixels_as_bytes = pixel_data_mv.tobytes ()
  pixels_as_list = list (pixels_as_bytes)
  pxs1 = list (chunks (pixels_as_list, 4))
  pxs2 = list (chunks (pxs1, pic_w))
  pxs = {}
  for y,pys in enumerate (pxs2):
    for x,pixel in enumerate (pys):
      pxs [x,y] = pixel
      
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
    cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (22)
  ct.set_source_rgb (0.0, 0.0, 0.0)
  
  te = ct.text_extents (numtext)
  # print (te)
  (x, y, w, h, dx, dy) = te
  w = dx/len (numtext)
  gen = generator1 (numtext)
  w = round (w)
  h = round (h) + 1
  # print (w,h)
  
  for y in range (0,int (pic_h-h),int (h)):
    s = ""
    for x in range (0,int (pic_w-w),int (w)):
      pts = []
      for y1 in range (0,int (h)):
        for x1 in range (0,int (w)):
          b,r,g,a = pxs [x+x1,y+y1]
          pts.append ((r+g+b)/3)
      avg = sum (pts) / len (pts)
      if avg < 128:
        s += next (gen)
      else:
        s += " "
    ct.move_to (0,y)
    ct.show_text (s)
    print (s)
  
  if outpic.endswith (".png"):
    surface.write_to_png (outpic)

for s in t:
  paint_pic (s,outpic)

