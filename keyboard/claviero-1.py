
"""
Use EAIONSTRLUCDPMVBGHFQXJYKZW from
~/interlingua/frequentia/litteras-in-ordine.txt
"""

import argparse
import textwrap
import cairo
import json
import time
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GLib
from gi.repository.GdkPixbuf import Pixbuf
from itertools import accumulate
from math import floor

imgfile = "imagine-claviero.png"
left,right = "left","right"
width = -1
height = 351
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
  pad ("-p", "--parolas", default="")
  pad ("-ln", "--line", type=int, default=-1)
  pad ("-wx", "--width", type=int, default=951)
  pad ("-hy", "--height", type=int, default=351)
  pad ("-ww", "--wrapwidth", type=int, default=75)
  pad ("-sz1", "--fontsize1", type=int, default=24)
  pad ("-sz2", "--fontsize2", type=int, default=20)
  pad ("--outlier", type=float, default=5.0)
  pad ("-font1", "--fontname1", default="UnDotum")
  pad ("-font2", "--fontname2", default="monospace")
  pad ("--hardwarecodes", action="store_true")
  pad ("--oldpic", action="store_true")
  pad ("--dontsave", action="store_true")
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
black = (0,0,0)
grays = [(x/10,x/10,x/10)for x in range(0,11)]
# print ("grays:")
# print (grays)
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
# blue = "#3771c8"
# red = "#d40000"

hardware_codes = [
  24,25,26,27,28,  29,30,31,32,33,34,
  38,39,40,41,42,  43,44,45,46,47,48,
  52,53,54,55,56,  57,58,59,60,61, ]

squares = [
  # upper row:
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
claves = [
  (24, 'V'),
  (25, 'L'),
  (26, 'D'),
  (27, 'C'),
  (28, 'X'),
  (29, 'K'),
  (30, 'M'),
  (31, 'U'),
  (32, 'Y'),
  (33, 'P'),
  (34, 'J'),
  (38, 'T'),
  (39, 'R'),
  (40, 'S'),
  (41, 'N'),
  (42, 'G'),
  (43, 'F'),
  (44, 'E'),
  (45, 'A'),
  (46, 'O'),
  (47, 'I'),
  (48, 'W'),
  (52, 'Q'),
  (53, 'H'),
  (54, 'B'),
  (55, 'Z'),
  (56, 'Å'),
  (57, 'Ö'),
  (58, 'Ä'),
  (59, ','),
  (60, '.'),
  (61, '-'),
]

special = {
  ',': ';',
  '.': ':',
  '-': '−'
}

sqs = {}
labels = {}

poss = {num: (side,x,y) for num,side,x,y in squares}
keyst = {num:ch for num,ch in claves}
shift = [(right,0,180,75,60),(right,736,180,165,60)]
for num,ch in claves:
  side,x1,y1 = poss [num]
  sqs[ch.lower()] = [(side,x1,y1,60,60)]
  labels[ch.upper()] = (side,num,x1,y1,60,60)
  if ch.isalpha(): 
    sqs[ch.upper()] = [(side,x1,y1,60,60)] + [shift[0 if side == right else 1]]

sqs[' '] = [(right,240,240,360,60)]
sqs['BackSpace'] = [(left,781,0,120,60)]

def init_vars (self):
  self.resline = ""
  self.current = ""
  self.old = ""
  self.nxt = ''
  self.last = ''
  self.restlen = 0
  self.total = 0
  self.starttime = None
  self.startkey = -1
  self.lastkept = 0
  self.presses = {}
  self.timeold = None
  self.rank = None
  self.curline = {}

def load_json_files (self):
  try:
    self.scores = json.load (open ("scores.json","r"))
    self.scores.sort (key=lambda y: (revers(y[0]), y[1]))
  except:
    self.scores = []
  try:
    self.results = json.load (open ("presses.json","r"))
  except:
    self.results = {}
  try:
    self.config = json.load (open ("config.json","r"))
  except:
    self.config = {'self.line': 0, 'self.usage':0}
  self.line = self.config ['self.line']
  if (not args.parolas) and 'self.curline' in self.config:
    self.curline = self.config ['self.curline']
    if args.infile in self.curline:
      self.line = self.curline [args.infile]
  self.usage = self.config ['self.usage']

def wrap_text (teksto):
  wrapper = textwrap.TextWrapper (width=args.wrapwidth)
  teksto = wrapper.wrap (text=teksto)
  teksto = [s + " " for s in teksto]
  return teksto

def load_teksto ():
  f = open (args.infile)
  teksto = f.read ()
  f.close ()
  
  rpl = ("\n"," "),("  "," "),("  "," "),
  for a,b in rpl:
    teksto = teksto.replace (a,b)
  
  # wrapper = textwrap.TextWrapper (width=args.wrapwidth)
  # teksto = wrapper.wrap (text=teksto)
  # teksto = [s + " " for s in teksto]
  # teksto = wrap_text (teksto)
  return teksto

def init_ui (self):
  self.pixbuf = Pixbuf.new_from_file_at_scale (
     imgfile, width, height, preserve_aspect_ratio)
  self.w,self.h = self.pixbuf.get_width (), self.pixbuf.get_height ()
  darea = Gtk.DrawingArea ()   
  darea.connect ("draw", self.on_draw)
  self.add (darea)
  self.resize (self.w, self.h+80)
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
  init_vars (self)
  load_json_files (self)
  if self.line >= len (self.text):
    self.line = 0
  if args.line != -1:
    self.line % len (self.text)
  # gdk_window = self.get_root_window()
  window = self.get_toplevel().get_window()
  window.set_cursor(Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR))

def draw_keys ():
  imgvacue = "claviero-vacue.png"
  surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, w_pic, h_pic)
  ct = cairo.Context (surface)
  font = args.fontname1
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  print ("Reading", imgvacue)
  im = cairo.ImageSurface.create_from_png (imgvacue)
  ct.set_source_surface(im, 0, 0)
  ct.paint()
  ct.set_font_size (args.fontsize1)
  th = args.fontsize1
  for value,side,x,y in baserow:
    ct.set_source_rgba (*(blue_cr if side == right else red_cr))
    ct.rectangle (x+25, y+25, 60, 60)
    ct.fill ()
  ct.set_source_rgb (0.0, 0.0, 0.0)
  ct.set_font_size (args.fontsize1)
  for ch in labels:
    side,num,x1,y1,h1,w1 = labels[ch]
    x,y = x1 + 25+7, y1 + 25+2
    ct.set_source_rgba (*(blue if side == right else red))
    ct.move_to (x,y+th)
    if args.hardwarecodes:
      ct.show_text (str(num))
    else:
      ct.show_text (ch)
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
  rest = current [len(gotright):]
  lft = sample0 [len(gotright):]
  return gotright, rest, lft

def draw_txt (x,y,ct,current,sample,gotright,rest,show_arrow=False):
  font = args.fontname2
  tsize = args.fontsize2 + 2
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

  ct.set_font_size (args.fontsize2)
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
  ct.show_text (rest)
  ct.set_source_rgb (*green)
  ct.show_text ('█')
  return nxt,len(rest)

def draw_res (ct,resline):
  font = args.fontname1
  fsize = args.fontsize2 - 4
  ct.set_font_size (fsize)
  ct.set_source_rgb (*black)
  ct.select_font_face (font, cairo.FONT_SLANT_NORMAL, 
      cairo.FONT_WEIGHT_BOLD)
  xbear, ybear, width, height, xadv, yadv = ct.text_extents(resline)
  ct.move_to (926-width,fsize + 2)
  ct.show_text (resline)

def calc_speed (self,chars):
  if not (self.starttime):
    self.starttime = time.time()
    self.startkey = chars - 1
    GLib.timeout_add (195, self.on_timeout)
    print ("Started.")
  if chars not in self.presses:
    self.presses [chars] = time.time() - self.starttime
    # print (chars)
  self.total = chars - self.startkey 
  # print (self.presses)

def period_results (self):
  pd = [0,1,2,3,4]
  ts = [0.5,1.0,1.5,2.0]
  now = time.time()
  seconds = now - self.starttime
  periodnow = seconds // 30
  remainder = floor (seconds % 30)
  p = {}
  for k,v in self.presses.items():
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
    self.presses = keep_small (self.presses,periodnow)
    # print ("presses in memory:",len(self.presses))
    print ("acclist:",acclist)
    if acclist.count(0) == 0:
      self.rank = save_score (self,cpm[3])
      print ("Score saved:",cpm[3])
    else:
      print ("Acclist contains zeros, score not saved.")
    self.lastkept = periodnow
  return cpm,p,seconds

def save_score (self,cpm3):
  # t1 = time.time()
  inx = 0
  for x,t in self.scores:
    if cpm3 > x:
      break
    else:
      inx += 1
  self.scores.insert (inx,[cpm3,time.strftime("%Y-%m-%d %H:%M:%S")])
  # t2 = time.time()
  # self.scores.sort (key=lambda y: (revers(y[0]), y[1]))
  # t3 = time.time()
  # print (f"time1: {t2-t1:.12f}")
  # print (f"time2: {t3-t2:.12f}")
  self.scores = self.scores [:15000]
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
  self.queue_draw ()

def draw_window (self, widget, cr):
  Gdk.cairo_set_source_pixbuf (cr, self.pixbuf, 0, 0)
  cr.paint ()
  gotright, rest,lft = calc_cire (self.current,self.text[self.line])
  this_and_some = [self.text [x % len(self.text)] 
    for x in range (self.line,self.line+5)]
  self.nxt,self.restlen = draw_txt (
    20,self.h+26,cr,self.current, this_and_some, gotright, rest,
    show_arrow=(not self.starttime))
  draw_res (cr,self.resline)
  bs = [] if self.restlen == 0 else sqs ['BackSpace']
  if self.nxt and self.nxt in sqs:
    for side,x,y,w,h in sqs [self.nxt] + bs:
      if self.restlen != 0:
        cr.set_source_rgba (*yellow_h)
        cr.rectangle (0, 0, w_pic, h_pic)
        cr.fill ()
      cr.set_source_rgba (*(blue_h if side == right else red_h))
      if gotright and lft and gotright[-1] == lft[0]:
        cr.set_line_width(6)
        cr.rectangle (x+25+3, y+25+3, w-6, h-6)
        cr.stroke ()
        cr.set_line_width(2)
      else:
        cr.rectangle (x+25, y+25, w, h)
        cr.fill ()
    self.last = self.nxt

def add_key (self):
  gotright, rest, lft = calc_cire (self.current,self.text[self.line])
  if rest == "" and self.current != self.old:
    calc_speed (self,self.wrappoints[self.line] + len(gotright))
    now = time.time ()
    if self.restlen == 0 and self.timeold:
      ad = (" " + self.current) [-2:]
      t1 = now - self.timeold
      if len (ad) == 2:
        if ad in self.results:
          a,b = self.results [ad] 
          if t1 / a < args.outlier:
            if b < 100:
              b += 1
            self.results [ad] = [(1/b) * t1 + (1 - 1/b) * a, b]
          else:
            # print ("Outlier rejected:", t1, "s", t1/a, "x")
            pass
        else:
          self.results [ad] = [t1,1]
        a,b = self.results [ad]
        # print (f"'{ad}': {a:.4f} s {b}")
    self.timeold = now
    self.old = self.current

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
    letter = letter.upper() if shift else letter.lower()
    if letter in special and shift:
      letter = special [letter]
    self.current += letter
  # print ("accept =",accept)
  if (not accept) and 0 <= number <= 512:
    self.current += chr (number)
  add_key (self)
  if self.restlen == 0 and len (self.current) >= len (self.text[self.line]):
    self.line = (self.line + 1) % len (self.text)
    self.current = ""
  widget.queue_draw ()

def do_quit (self,widget,event):
  if self.starttime:
    self.usage += round (time.time() - self.starttime)
  if not args.parolas:
    self.curline [args.infile] = self.line 
  self.config = {'self.line': self.line, 'self.usage': self.usage,
    'self.curline': self.curline}
  if not args.dontsave:
    json.dump (self.config, open("config.json","w"))
    json.dump (self.results, open("presses.json","w"))
    json.dump (self.scores, open("scores.json","w"))
  else:
    print ("Argument '--dontsave': Nothing has been saved.")
  print ("Number of scores =",len(self.scores))
  print ("Best scores:")
  for x,t in self.scores[:30]:
    print (f"{x:>7.1f} {t}")
  print ("Quitting.")
  # print ("Total usage:", self.usage, "seconds.")
  m, s = divmod (self.usage, 60)
  h, m = divmod (m, 60)
  print ("Total usage:", h, "hours", m, "minutes.")
  Gtk.main_quit()

if not args.oldpic:
  draw_keys ()

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
    return True # True = continue calling
  def on_key_press (self, widget, event):
    handle_key_press (self, widget, event)

win = Win ()
Gtk.main ()

