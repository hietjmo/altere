
"""
python claviero-1.py --ordine /vldcxkmuypj/trsngfeaoiw/qhbzåöä,.-/ --keycapfont UnDotum --keycapfontsize 24
python claviero-1.py -order "/vldcxkmuypj/trsngfeaoiw/qhbzåöä,.-/" --createpic
Use EAIONSTRLUCDPMVBGHFQXJYKZW from
~/interlingua/frequentia/litteras-in-ordine.txt
"""

import argparse
import textwrap
import random
import cairo
import json
import time
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GLib
from gi.repository.GdkPixbuf import Pixbuf
from itertools import accumulate
from collections import defaultdict
from os.path import exists
from math import floor

imgfile = "imagine-claviero.png"
left,right,number,kgreen = "left","right","number","kgreen"
width = -1
height = 352
preserve_aspect_ratio = True

class revers:
  def __init__(self, obj):
    self.obj = obj
  def __eq__(self, other):
    return other.obj == self.obj
  def __lt__(self, other):
    return other.obj < self.obj

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-i", "--infile", default="crusoe-de-novo-ia.txt")
  pad ("-order", "--ordine", default="")
  pad ("-p", "--parolas", default="")
  pad ("-ln", "--line", type=int, default=-1)
  pad ("-wx", "--width", type=int, default=952)
  pad ("-hy", "--height", type=int, default=352)
  pad ("-ww", "--wrapwidth", type=int, default=75)
  pad ("-cpm", "--insectspeed", type=float, default=-1.0)
  pad ("-sz1", "--keycapfontsize", type=int, default=20)
  # pad ("-sz1", "--fontsize2", type=int, default=24)
  pad ("-sz2", "--resultlinefontsize", type=int, default=16)
  pad ("-sz3", "--writesamplefontsize", type=int, default=20)
  pad ("--outlier", type=float, default=5.0)
  pad ("-font1", "--keycapfont", default="sans-serif")
  pad ("-font2", "--resultlinefont", default="sans-serif")
  # pad ("-font1", "--fontname2", default="UnDotum")
  pad ("-font3", "--writesamplefont", default="monospace")
  pad ("--hardwarecodes", action="store_true")
  pad ("--createpic", action="store_true")
  pad ("--dontsave", action="store_true")
  pad ("--no_insects", action="store_true")
  for i in range (0,10):
    pad (f"--log{i}", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()
w_pic, h_pic = args.width,args.height

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
pink = (1.00, 0.9, 0.9)
orange = (0.996, 0.878, 0.761)
green = (0.220, 0.780, 0.278)
purple = (0.561, 0.220, 0.780)
yellow = (0.988,0.918,0.169)
black = (0,0,0)
grays = [(x/10,x/10,x/10)for x in range(0,11)]
gray = grays[4]
gray_h = gray + (0.60,)
white = (1,1,1)
orange2 = orange + (0.60,)
blue = 0.22, 0.44, 0.78
red = 0.83, 0.00, 0.00
blue_cr =  blue + (0.20,)
red_cr = red + (0.20,)
blue_h = blue + (0.60,)
red_h = red + (0.60,)
green_h = green + (0.60,)
yellow_h = yellow + (0.60,)
purple_h = purple + (0.60,)

def hex_to_rgb (hex):
  h = hex.lstrip('#')
  return tuple (int (h[i:i+2], 16) / 255 for i in (0, 2, 4))

favs = [hex_to_rgb (openmojipalette [name]) for name in [
  'blue','red','green','orange','grey','pink','purple','NavyBlue','Maroon' ]]
random.shuffle (favs)

hardware_codes = [
  10,11,12,13,14,  15,16,17,18,19,
  24,25,26,27,28,  29,30,31,32,33,34,
  38,39,40,41,42,  43,44,45,46,47,48,
  52,53,54,55,56,  57,58,59,60,61, 
]

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
# d = {(b,c): a for a,(b,c,d,e) in list (zip (hardware_codes, squares))}
w,h = 60,60

# EAION STRLU CDPMV BGHFQ XJYKZ W
"""
claves = [
  # number row:
  (10, '1'), (11, '2'), (12, '3'), (13, '4'), (14, '5'), 
  (15, '6'), (16, '7'), (17, '8'), (18, '9'), (19, '0'), 
  # upper row:
  (24, 'V'), (25, 'L'), (26, 'D'), (27, 'C'), (28, 'X'), 
  (29, 'K'), (30, 'M'), (31, 'U'), (32, 'Y'), (33, 'P'), (34, 'J'),
  # middle row:
  (38, 'T'), (39, 'R'), (40, 'S'), (41, 'N'), (42, 'G'), 
  (43, 'F'), (44, 'E'), (45, 'A'), (46, 'O'), (47, 'I'), (48, 'W'),
  # bottom row:
  (52, 'Q'), (53, 'H'), (54, 'B'), (55, 'Z'), (56, 'Å'), 
  (57, 'Ö'), (58, 'Ä'), (59, ','), (60, '.'), (61, '-'),
]
"""

def create_order (self):
  global sqs, shift, keyst, special, labels
  # order = "/vldcxkmuypj/trsngfeaoiw/qhbzåöä,.-/"
  order = "/qwertyuiopå/asdfghjklöä/zxcvbnm,.-/"
  if self.order:
    order = self.order
  if args.ordine:
    order = args.ordine
  ao = order.split(order[0])
  print ("--ordine",order)
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
  if args.createpic or args.ordine or order != self.order or not exists (imgfile):
    print ("Create new key order.")
    self.order = args.ordine
    draw_key_image ()

def init_vars (self):
  self.resline, self.oldresline = "",""
  self.current, self.old = "",""
  self.nxt, self.last = '',''
  self.restlen, self.total = 0,0
  self.startkey = -1
  self.lastkept = 0
  self.latter = {}
  self.starttime, self.timeold, self.rank = None,None,None
  self.curline = {}
  self.errors = defaultdict (lambda: 0)
  self.lasterror = 0,0
  self.outliers = []

def load_json_files (self):
  try:
    self.scores = json.load (open ("scores.json","r"))
    self.scores.sort (key=lambda y: (revers(y[0]), y[1]))
  except:
    self.scores = []
  self.insectspeed = args.insectspeed
  if self.scores:
    self.insectspeed = self.scores [0][0]
  if args.insectspeed > 0.0:
    self.insectspeed = args.insectspeed 
  print ("self.insectspeed =", self.insectspeed)
  try:
    self.presses = json.load (open ("presses.json","r"))
  except:
    self.presses = {}
  try:
    self.config = json.load (open ("config.json","r"))
  except:
    self.config = {'line': 0, 'usage':0, 'alltimekeys':0}
  self.line = self.config ['line']
  if (not args.parolas) and 'curline' in self.config:
    self.curline = self.config ['curline']
    if args.infile in self.curline:
      self.line = self.curline [args.infile]
  if 'order' in self.config:
    self.order = self.config ['order']
  else:
    self.order = ""
  self.usage = self.config ['usage']
  self.alltimekeys = self.config ['alltimekeys']

def wrap_text (teksto):
  wrapper = textwrap.TextWrapper (width=args.wrapwidth)
  teksto = wrapper.wrap (text=teksto)
  teksto = [s + " " for s in teksto]
  return teksto

def load_teksto ():
  f = open (args.infile)
  teksto = f.read().strip()
  f.close ()
  rpl = ("\n"," "),("  "," "),("  "," "),
  for a,b in rpl:
    teksto = teksto.replace (a,b)
  # print (teksto)
  return teksto

def init_ui (self):
  init_vars (self)
  load_json_files (self)
  create_order (self)
  self.pixbuf = Pixbuf.new_from_file_at_scale (
     imgfile, width, height, preserve_aspect_ratio)
  self.w,self.h = self.pixbuf.get_width (), self.pixbuf.get_height ()
  darea = Gtk.DrawingArea ()   
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, 10, 10)
  ct = cairo.Context (surface)
  font = args.writesamplefont
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_NORMAL)
  ct.set_font_size (args.writesamplefontsize)
  xbear, ybear, w4, h4, xadv, yadv = ct.text_extents(100*"x")
  self.charw = w4 / 100
  # print ("self.charw  =",self.charw )
  darea.connect ("draw", self.on_draw)
  self.add (darea)
  self.resize (self.w, self.h+85)
  self.connect ("delete-event", self.on_quit)
  self.connect ("key-press-event",self.on_key_press)
  self.set_position(Gtk.WindowPosition.CENTER)
  self.show_all ()
  if args.parolas:
    self.text = 50 * (args.parolas + " ")
  else:
    self.text = load_teksto ()
  self.text = wrap_text (self.text)
  self.wrappoints = list (accumulate([0]+[len (s) for s in self.text]))
  if self.line >= len (self.text):
    self.line = 0
  if args.line != -1:
    self.line % len (self.text)
  # gdk_window = self.get_root_window()
  window = self.get_toplevel().get_window()
  window.set_cursor(Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR))

def label_color (side):
  d = {right:blue, left:red, number:gray, kgreen: green}
  return d [side]

def hilit_color (side):
  d = {right:blue_h, left:red_h, number:gray_h, kgreen: green_h}
  return d [side]

def draw_key_image ():
  imgvacue = "claviero-vacue.png"
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct = cairo.Context (surface)
  font = args.keycapfont
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  th = args.keycapfontsize
  ct.set_font_size (args.keycapfontsize)

  print ("Reading", imgvacue)
  if exists (imgvacue):
    im = cairo.ImageSurface.create_from_png (imgvacue)
  else:
    im = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct.set_source_surface(im, 0, 0)
  ct.paint()

  for value,side,x,y in baserow:
    ct.set_source_rgba (*(blue_cr if side == right else red_cr))
    ct.rectangle (x+25, y+25, 60, 60)
    ct.fill ()
  ct.set_source_rgb (0.0, 0.0, 0.0)
  # ct.set_font_size (args.keycapfontsize)
  for ch in labels:
    side,num,x1,y1,h1,w1 = labels[ch]
    x,y = x1 + 25+7, y1 + 25+2
    ct.set_source_rgba (*(label_color(side)))
    ct.move_to (x,y+th)
    if args.hardwarecodes:
      ct.show_text (str(num))
    else:
      if side == number:
        ct.move_to (x,y+60-10)
      ct.show_text (ch)
  print ("Writing", imgfile)
  surface.write_to_png (imgfile)

def keep_small (d,periodnow):
  result = {}
  for k,v in d.items():
    period = periodnow - v // 30
    if 0 <= period <= 4:
      result[k] = v
  return (result)

def same (s1,s2):
  x = 0
  while len(s1) > x and len (s2) > x and s1 [x] == s2 [x]:
    x += 1
  return x

def calc_cire (current,sample0):
  sams = same (current,sample0)
  gotright = sample0 [:sams]
  gotwrong = current [len(gotright):]
  lft = sample0 [len(gotright):]
  return gotright, gotwrong, lft

def draw_txt (x,y,ct,current,sample,gotright,gotwrong,show_arrow=False):
  font = args.writesamplefont
  tsize = args.writesamplefontsize + 2
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_NORMAL)
  if show_arrow:
    ct.set_font_size (10)
    ct.set_source_rgb (*red)
    ct.move_to (3,y+1*tsize)
    ct.show_text ("1")
    ct.set_source_rgb (*red)
    ct.move_to (3,y+0*tsize)
    ct.show_text ("2")

  ct.set_font_size (args.writesamplefontsize)
  sams = same (current,sample[0])
  padded = sample[0] if sams == 0 else " " * sams + sample[0] [sams:]
  ct.set_source_rgb (*black)
  ct.move_to (x,y+tsize)
  ct.show_text (padded)

  ct.set_source_rgb (*grays[2])
  ct.move_to (x,y)
  ct.show_text (sample[1])

  ct.set_source_rgb (*black)
  ct.move_to (x,y+2*tsize)
  ct.show_text (gotright)

  lft = sample[0] [len(gotright):]
  nxt = lft [:1]
  ct.set_source_rgb (*red)
  ct.show_text (gotwrong)
  ct.set_source_rgb (*green)
  ct.show_text ('█')
  return nxt,len(gotwrong)

def draw_res (ct,resline):
  font = args.resultlinefont
  fsize = args.resultlinefontsize
  ct.set_font_size (fsize)
  ct.set_source_rgb (*black)
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  xbear, ybear, width, height, xadv, yadv = ct.text_extents(resline)
  ct.move_to (926-width,fsize + 2)
  ct.show_text (resline)

def save_resultlog (self,wtot):
  print ("save_resultlog")
  r = defaultdict (lambda: [])
  for k,v in self.presses.items():
    if len(k) == 2:
      a,b = k[0],k[1]
      if a != b and 'a' <= b <= 'z':
        r[b].append (v)
  q = []
  for k,v in r.items():
    c,d = v[0]
    for a,b in v:
      c,d = (c * d + a * b) / (d + b), d + b
    q.append ((k,c))
  
  q.sort (key=lambda x: x[1])
  f = open ("resultlog.txt","a")
  f.write (f"# {wtot}\n")
  for a,b in q:
    f.write (f"{a} {b:.4f}\n")
  f.close()

def calc_speed (self,chars):
  if not (self.starttime):
    self.starttime = time.time()
    self.startkey = chars - 1
    GLib.timeout_add (195, self.on_timeout)
    print ("Started.")
  if chars not in self.latter:
    self.latter [chars] = time.time() - self.starttime
    # print (chars)
  self.total = chars - self.startkey 
  wtot = self.alltimekeys + self.total
  # if args.log3:
  #  print (wtot)
  if wtot % 25000 == 0:
    save_resultlog (self,wtot)
  # print (self.latter)

def period_results (self):
  pd = [0,1,2,3,4]
  ts = [0.5,1.0,1.5,2.0]
  now = time.time()
  seconds = floor (now - self.starttime)
  periodnow = seconds // 30
  remainder = seconds % 30
  p = {}
  for k,v in self.latter.items():
    period = periodnow - v // 30
    for pe in pd:
      if pe not in p:
        p[pe] = 0
      if pe == period: 
        p[pe] += 1
  acclist = []
  for x in pd[1:]:
    if x in p:
      acclist.append (p[x])
    else:
      acclist.append (0)
  acc = list (accumulate (acclist))
  cpm = [a/b for a,b in zip (acc,ts)]
  if remainder == 0 and self.lastkept != periodnow:
    self.rank = None
    self.latter = keep_small (self.latter,periodnow)
    if args.log3:
      print ("latter in memory:",len(self.latter))
      print ("acclist:",acclist)
    if acclist.count(0) == 0:
      self.rank = save_score (self,cpm[3])
      print (f"Score saved: {cpm[3]} ({self.rank})")
    else:
      print ("Acclist contains zeros, score not saved.")
    self.lastkept = periodnow
  return cpm,p,seconds

def save_score (self,cpm3):
  inx = 0
  for x,t in self.scores:
    if cpm3 > x:
      break
    else:
      inx += 1
  self.scores.insert (inx,[cpm3,time.strftime("%Y-%m-%d %H:%M:%S")])
  self.scores = self.scores [:15000]
  if cpm3 > self.insectspeed:
    self.insectspeed = cpm3
    print ("self.insectspeed =", self.insectspeed)
  return inx + 1

def take_timeout (self):
  # print ("Timeout.")
  cpm,p,seconds = period_results (self)
  self.resline = " ".join (
    [str(p[0]) if 0 in p else ""] + 
    [str(self.total)] + 
    [f"{x:.1f}" for x in cpm] + 
    [("(" + str(self.rank) + ")") if self.rank else ""] + 
    [(str(floor(seconds / 60)).zfill (2) 
      + ":" + str(floor(seconds % 60)).zfill (2))]) 
  if args.log5:
    if self.oldresline != self.resline:
      print (self.resline)
      self.oldresline = self.resline
  self.queue_draw ()

def paint_insects (self,ct):
  if self.starttime and not args.no_insects:
    tme = time.time() - self.starttime
    insectspace = self.w / len (favs)
    for i,color in enumerate (favs):
      ct.set_source_rgb (*color)
      # print (self.charw)
      # print (self.insectspeed)
      # print (tme)
      s1 = self.charw * (self.insectspeed * tme / 60)
      ct.rectangle ((s1+insectspace*i)%self.w, self.h+80, 20, 5)
      ct.fill ()

def draw_window (self, widget, cr):
  Gdk.cairo_set_source_pixbuf (cr, self.pixbuf, 0, 0)
  cr.paint ()
  gotright,gotwrong,lft = calc_cire (self.current,self.text[self.line % len (self.text)])
  this_and_some = [self.text [x % len(self.text)] 
    for x in range (self.line,self.line+5)]
  self.nxt,self.gotwronglen = draw_txt (
    20,self.h+26,cr,self.current, this_and_some, gotright, gotwrong,
    show_arrow=(not self.starttime))
  draw_res (cr,self.resline)
  paint_insects (self,cr)
  bs = [] if self.gotwronglen == 0 else sqs ['BackSpace']
  if self.nxt and self.nxt in sqs:
    for side,x,y,w,h in sqs [self.nxt] + bs:
      if self.gotwronglen != 0:
        cr.set_source_rgba (*yellow_h)
        cr.rectangle (0, 0, w_pic, h_pic)
        cr.fill ()
      cr.set_source_rgba (*(hilit_color(side)))
      if gotright and lft and gotright[-1] == lft[0]:
        cr.set_line_width(6)
        cr.rectangle (x+25+3, y+25+3, w-6, h-6)
        cr.stroke ()
        cr.set_line_width(2)
      else:
        cr.rectangle (x+25, y+25, w, h)
        cr.fill ()
    self.last = self.nxt

def divmod_wrappoint (wrappoints, line):
  q,r = divmod (line, len(wrappoints)-1)
  result = q * wrappoints [-1] + wrappoints [r]
  if args.log4:
    print ("line", line, end=", ")
    print ("len wp", len(wrappoints)-1, end=", ")
    print ("q",q, end=", ")
    print ("r",r, end=", ")
    print ("result",result)
  return result


def add_key (self):
  gotright,gotwrong,lft = calc_cire (self.current,self.text[self.line % len (self.text)])
  if gotwrong == "" and self.current != self.old:
    calc_speed (self,divmod_wrappoint (self.wrappoints,self.line) + len(gotright))
    now = time.time ()
    if self.gotwronglen == 0 and self.timeold:
      ad = (" " + self.current) [-2:]
      t1 = now - self.timeold
      if len (ad) == 2:
        if ad in self.presses:
          a,be = self.presses [ad] 
          if t1 / a < args.outlier:
            be += 1
            b = min (300,be)
            self.presses [ad] = [(1/b) * t1 + (1 - 1/b) * a, be]
          else:
            out = (ad,t1,t1/a)
            self.outliers.append (out)
            if args.log2:
              print (f"Outlier rejected: '{out[0]}' {out[1]:.4f} s {out[2]:.2f}x")
        else:
          self.presses [ad] = [t1,1]
        if args.log2:
          a,be = self.presses [ad]
          print (f"'{ad}': {a:.4f} s {be}")
    self.timeold = now
    self.old = self.current
  else:
    if len(gotwrong) == 1 and self.starttime:
      newerror = self.line, len(gotright)
      if newerror != self.lasterror:
        now = time.time()
        seconds = floor (now - self.starttime)
        periodnow = seconds // 30
        # print ("error:", periodnow,newerror)
        self.errors[periodnow] += 1
        self.lasterror = newerror
        # print (dict(self.errors))

def letter_shift (letter,shift):
  if letter.isalpha():
    return letter.upper() if shift else letter.lower() 
  return letter

def handle_key_press (self, widget, event):
  hw2 = event.hardware_keycode
  number = event.keyval
  keyname = Gdk.keyval_name (event.keyval)
  shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
  ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
  accept = False
  if ctrl and keyname == "d":
    print ("Control-D pressed. Quitting.")
    self.on_quit (widget, event)
  if keyname == "space":
    # print ("space")
    accept = True
    self.current += " "
  if keyname == "BackSpace":
    # print ("BackSpace")
    accept = True
    self.current = self.current [:-1]
  if hw2 in hardware_codes:
    # print (hw2, ":", hw1 [hw2])
    letter = keyst [hw2]
    accept = letter != ''
    # print (f"letter ='{letter}'")
    if letter in special and shift:
      letter = special [letter]
    letter = letter_shift (letter,shift)
    self.current += letter
  # print ("accept =",accept)
  if (not accept) and 0 <= number <= 512:
    self.current += chr (number)
  add_key (self)
  if self.current == self.text[self.line % len (self.text)]:
    self.line += 1
    self.current = ""
  widget.queue_draw ()

def do_quit (self,widget,event):
  self.alltimekeys += self.total
  if self.starttime:
    self.usage += round (time.time() - self.starttime)
  if not args.parolas:
    self.curline [args.infile] = self.line % len (self.text)
  self.config = {'line': self.line % len (self.text), 'usage': self.usage,
    'curline': self.curline, 'alltimekeys': self.alltimekeys, 
    'order': self.order }
  if not args.dontsave:
    json.dump (self.config, open("config.json","w"))
    json.dump (self.presses, open("presses.json","w"))
    json.dump (self.scores, open("scores.json","w"))
  else:
    print ("Argument '--dontsave': Nothing has been saved.")
  print ("Outliers:")
  for out in self.outliers:
    print (f"'{out[0]}' {out[1]:.4f} s {out[2]:.2f}x")
  print ("Number of scores =",len(self.scores))
  print ("Best scores:")
  for x,t in self.scores[:30]:
    print (f"{x:>7.1f} {t}")
  print ("Quitting.")
  # print ("Total usage:", self.usage, "seconds.")
  m, s = divmod (self.usage, 60)
  h, m = divmod (m, 60)
  print ("Total usage:", h, "hours", m, "minutes.")
  print ("Total keys:", self.alltimekeys)
  Gtk.main_quit()

class Win (Gtk.Window):
  def __init__ (self):
    super (Win, self).__init__()
    init_ui (self)
  def on_quit (self, widget, event):
    do_quit (self,widget,event)
    return False
  def on_draw (self, widget, cr):
    draw_window (self, widget, cr)
  def on_timeout (self):
    take_timeout (self)
    return True # True means continue calling
  def on_key_press (self, widget, event):
    handle_key_press (self, widget, event)

win = Win ()
Gtk.main ()

