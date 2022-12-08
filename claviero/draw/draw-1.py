
# python draw-1.py --bright

import argparse
import os
import shutil
import cairo
from cairosvg import svg2png

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument

  pad ("--imgfile", default="claviero-3.png")
  pad ("--order",default="/qwertyuiopå/asdfghjklöä/zxcvbnm,.-/")
  pad ("--empty", action="store_true")
  pad ("--qwerty", action="store_true")
  pad ("--dlpm", action="store_true")
  pad ("--bright", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

openmojipalette = {
  'blue': '#92d3f5', 'blueshadow': '#61b2e4', 'red': '#ea5a47', 'redshadow': '#d22f27', 
  'green': '#b1cc33', 'greenshadow': '#5c9e31', 'yellow': '#fcea2b', 'yellowshadow': '#f1b31c', 
  'white': '#ffffff', 'lightgrey': '#d0cfce', 'grey': '#9b9b9a', 'darkgrey': '#3f3f3f', 
  'black': '#000000', 'orange': '#f4aa41', 'orangeshadow': '#e27022', 
  'pink': '#ffa7c0', 'pinkshadow': '#e67a94', 'purple': '#b399c8', 'purpleshadow': '#8967aa', 
  'brown': '#a57939', 'brownshadow': '#6a462f', 
  'LightSkinTone': '#fadcbc', 'MediumLightSkinTone': '#debb90', 'MediumSkinTone': '#c19a65', 
  'MediumDarkSkinTone': '#a57939', 'DarkSkinTone': '#6a462f', 'DarkSkinShadow': '#352318', 
  'NavyBlue': '#1e50a0', 'Maroon': '#781e32', 'DarkGreen': '#186648'}

def hex_to_rgb (hex):
  h = hex.lstrip('#')
  return tuple (int (h[i:i+2], 16) / 255 for i in (0, 2, 4))

favs = [hex_to_rgb (openmojipalette [name]) for name in [
  'purple','green','orange','grey','blue','red','pink','NavyBlue','Maroon' ]]
# random.shuffle (favs)

def om (name):
  return hex_to_rgb (openmojipalette [name])

eb_gris = (0.337,0.361,0.396)
pink = (1.00, 0.9, 0.9)
orange = (0.996, 0.878, 0.761)
# green = (0.220, 0.780, 0.278)
purple = (0.561, 0.220, 0.780)
yellow = (0.988,0.918,0.169)
black = (0,0,0)
grays = [(x/10,x/10,x/10)for x in range(0,11)]
gray = grays[4]
gray_h = gray + (0.60,)
white = (1,1,1)
orange2 = orange + (0.60,)
# blue = 0.22, 0.44, 0.78
# red = 0.83, 0.00, 0.00

green = om ("green")
blue = om ("blue")
red = om ("pink")

#blue_cr =  blue + (0.20,)
#red_cr = red + (0.20,)

xl,lxx = (0.30,),(0.70,)
blue_cr =  blue + xl
red_cr = red + xl

blue_h = blue + lxx
red_h = red + lxx
green_h = green + lxx


yellow_h = yellow + lxx
purple_h = purple + lxx

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

color = {0:black,1:grays[2],"bg":grays[5]}
color = {
  0:grays[10],1:grays[9],
  "bg":grays[2],"cr":om("green"),
  3:grays[9],4:grays[9],5:grays[9],
  7:om("green"),8:om("purple"),9:grays[9],
  "danger":om("blue") + xl
}

w_pic, h_pic = 952,352
font1 = "Swiss 721"
font2 = "DejaVu Sans"
font3 = "Unifont"

alphabeto = [
  ('A', 'aquila', 'Aquila'),
  ('B', 'balena', 'Balena'),
  ('C', 'catto', 'Catto'),
  ('D', 'dinosauro', 'Dinosauro'),
  ('E', 'elephante', 'Elephante'),
  ('F', 'flamingo', 'Flamingo'),
  ('G', 'girafa', 'Girafa'),
  ('H', 'hippopotamo', 'Hippopotamo'),
  ('I', 'iguana', 'Iguana'),
  ('J', 'jaguar', 'Jaguar'),
  ('K', 'kanguru', 'Kanguru'),
  ('L', 'leon', 'Leon'),
  ('M', 'mus', 'Mus'),
  ('N', 'narval', 'Narval'),
  ('O', 'octopode', 'Octopode'),
  ('P', 'pinguin', 'Pinguin'),
  ('Q', 'qualia', 'Qualia'),
  ('R', 'ratto', 'Ratto'),
  ('S', 'scuriolo', 'Scuriolo'),
  ('T', 'tigre', 'Tigre'),
  ('U', 'unicornio', 'Unicornio'),
  ('V', 'vipera', 'Vipera'),
  ('W', 'wombat', 'Wombat'),
  ('X', 'xenopo', ['Xenopo', '(rana african)']),
  ('Y', 'yak', 'Yak'),
  ('Z', 'zebra', 'Zebra'),
]


boxes = (
  [(25,60*y+25,850 if y == 2 else 925,60*y+25) for y in range (6)] +
  [(60*x+85,25,60*x+85,60+25) for x in range (13)] +
  [(60*x+115,60+25,60*x+115,120+25) for x in range (13)] +
  [(60*x+130,120+25,60*x+130,180+25) for x in range (13)] + 
  [(60*x+100,180+25,60*x+100,240+25) for x in range (12)] +
  [(x,240+25,x,300+25) for x in [115,175,265,625,715,775,835]] +
  [(25,25,25,325),(925,25,925,325)]
  )
specials = [
  ("Backspace",830,70),
  ("Tab",34,123),
  ("Caps",34,170),
  ("Lock",34,188),
  ("Shift",34,245),
  ("Control",40,300),
  ("Alt",207,300),
  ("Alt Gr",646,300),
  ("Enter",875,105),
  ("Shift",852,245),
  ("Control",850,300),
]
symbols = [
  ("⟵",860,58),
  ("↹",70,128),
  ("⇫",85,188),
  ("⇧",67,249),
  ("↵",880,145),
  ("⇧",885,249),
]
animales = [
  ("deer",30,31),
  ("cow-face",752,31),
  ("front-facing-baby-chick",781,91),
  ("turtle",795,150),
  ("dog-face",864,150),
  ("elephant",105,214),
  ("ewe",780,214),
  ("cat",122,274),
  ("cat",722,274),
  ("rabbit",780,270),
]

hardware_codes = [
  10,11,12,13,14,  15,16,17,18,19,
  24,25,26,27,28,  29,30,31,32,33,34,
  38,39,40,41,42,  43,44,45,46,47,48,
  52,53,54,55,56,  57,58,59,60,61, 
]
left,right,number,kgreen = "left","right","number","kgreen"
squares = [
  # number row: 85-25,85-25
  (10, number, 60, 0),
  (11, number, 120, 0),
  (12, number, 180, 0),
  (13, number, 240, 0),
  (14, number, 300, 0),
  (15, number, 360, 0),
  (16, number, 420, 0),
  (17, number, 480, 0),
  (18, number, 540, 0),
  (19, number, 600, 0),
  (20, number, 660, 0),
  # upper row: 115-25,85-25
  (24, left, 90, 60),
  (25, left, 150, 60),
  (26, left, 210, 60),
  (27, left, 270, 60),
  (28, left, 330, 60),
  (29, right, 390, 60),
  (30, right, 450, 60),
  (31, right, 510, 60),
  (32, right, 570, 60),
  (33, right, 630, 60),
  (34, right, 690, 60),
  # middle row:
  (38, left, 105, 120),
  (39, left, 165, 120),
  (40, left, 225, 120),
  (41, left, 285, 120),
  (42, left, 345, 120),
  (43, right, 405, 120),
  (44, right, 465, 120),
  (45, right, 525, 120),
  (46, right, 585, 120),
  (47, right, 645, 120),
  (48, right, 705, 120),
  # bottom row:
  (52, left, 135, 180),
  (53, left, 195, 180),
  (54, left, 255, 180),
  (55, left, 315, 180),
  (56, left, 375, 180),
  (57, right, 435, 180),
  (58, right, 495, 180),
  (59, right, 555, 180),
  (60, right, 615, 180),
  (61, right, 675, 180),
]

baserow = [
  # left:
  (38, left, 105, 120),
  (39, left, 165, 120),
  (40, left, 225, 120),
  (41, left, 285, 120),
  # right:
  (44, right, 465, 120),
  (45, right, 525, 120),
  (46, right, 585, 120),
  (47, right, 645, 120),
]
w,h = 60,60
hardwarecodes = False

# EAION STRLU CDPMV BGHFQ XJYKZ W

def create_order ():
  global sqs, shift, keyst, special, labels
  order = args.order
  if args.dlpm:
    order = "/dlpmfwcuygj/trsnvqeaoik/xbzhåöä,.-/"
  if args.qwerty:
    order = "/qwertyuiopå/asdfghjklöä/zxcvbnm,.-/"
  ao = order.split (order[0])
  claves = (
    # number row:
    [(10+i,x) for i,x in enumerate ("1234567890+")] +
    # upper row:
    [(24+i,x.upper()) for i,x in enumerate (ao[1])] +
    # middle row:
    [(38+i,x.upper()) for i,x in enumerate (ao[2])] +
    # bottom row:
    [(52+i,x.upper()) for i,x in enumerate (ao[3])]
  )
  
  special = {
    ',': ';', '.': ':', '-': '−', '1': '!', '2': '"', 
    '3': '#', '5': '%', '7': '/', '8': '(', '9': ')',
  }
  
  sqs = {}
  labels = {}
  
  poss = {num: (side,x,y) for num,side,x,y in squares}
  keyst = {num:ch for num,ch in claves}
  shift = [(kgreen,0,180,75,60),(kgreen,736,180,165,60)]
  for num,ch in claves:
    side,x1,y1 = poss [num]
    sqs[ch.lower()] = [(side,x1,y1,60,60)]
    labels[ch.upper()] = (side,num,x1,y1,60,60)
    if ch.isalpha(): 
      sqs[ch.upper()] = [(side,x1,y1,60,60)] + [shift[0 if side == right else 1]]
  
  sqs[' '] = [(kgreen,240,240,360,60)]
  sqs['BackSpace'] = [(kgreen,781,0,120,60)]

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)

def create_animales ():
  crear ("png")
  for s,x,y in animales:
    filename = "alfabeto-svg/" + s + '.svg'
    outpic = "png/" + s + ".png"
    svg2png (
      url=filename,
      parent_width=46,
      parent_height=46,
      write_to=outpic
    )

def draw_animales (ct):
  for s,x,y in animales:
    inpic = "png/" + s + ".png"

    im = cairo.ImageSurface.create_from_png (inpic)
    ct.set_source_surface (im, x, y)
    ct.paint ()

def label_color (side):
  d = {right:blue, left:red, number:gray, kgreen: green}
  return d [side]

def draw_baserow (ct):
  for value,side,x,y in baserow:
    # ct.set_source_rgba (*(blue_cr if side == right else red_cr))
    if args.bright:
      ct.set_source_rgb (*grays[8])
    else:
      ct.set_source_rgba (*blue_cr)
    ct.rectangle (x+25, y+25, 60, 60)
    ct.fill ()

def draw_keys (ct):
  ct.select_font_face (font1, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  th = 18
  ct.set_font_size (th)
  for ch in labels:
    side,num,x1,y1,h1,w1 = labels[ch]
    x,y = x1 + 25+8, y1 + 25+3
    # ct.set_source_rgba (*(label_color(side)))
    if args.bright:
      ct.set_source_rgb (*eb_gris)
    else:
      ct.set_source_rgb (*grays[7])
    ct.move_to (x,y+th)
    if hardwarecodes:
      ct.show_text (str(num))
    else:
      if side == number:
        ct.move_to (x,y+60-10)
      ct.show_text (ch)

def create_canvas ():
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct = cairo.Context (surface)
  ct.set_line_width (1.05)
  if args.bright:
    ct.set_source_rgb (*grays[9])
  else:
    ct.set_source_rgb (*eb_gris)
  ct.paint ()
  if args.bright:
    ct.set_source_rgb (*white)
  else:
    ct.set_source_rgb (*color["bg"])
  ct.rectangle (25,25,900,300)
  ct.fill ()
  return ct,surface

def draw_base (ct):
  ct.select_font_face (font1, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (16)
  if args.bright:
    ct.set_source_rgb (*eb_gris)
  else:
    ct.set_source_rgb (*gris)
  for x1,y1,x2,y2 in boxes:
    ct.move_to (x1,y1)
    ct.line_to (x2,y2)
  ct.stroke ()

  for s,x,y in specials:
    ct.move_to (x,y)
    ct.show_text (s)

  ct.select_font_face (font2, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  ct.set_font_size (40)

  for s,x,y in symbols:
    ct.move_to (x,y)
    ct.show_text (s)
  return ct,surface

create_order () 
create_animales ()
ct,surface = create_canvas ()
draw_animales (ct)
draw_baserow (ct)
if not args.empty:
  draw_keys (ct)
draw_base (ct)
print ("Writing", args.imgfile)
surface.write_to_png (args.imgfile)

# print (boxes)

