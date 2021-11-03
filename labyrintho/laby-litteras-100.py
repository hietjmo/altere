#!/usr/bin/env python

import random
import cairo
from math import *
from collections import defaultdict

class Puncto:
  def __init__ (self, x=0, y=0):
    self.x = x
    self.y = y
  def __repr__ (self):
    return f"Puncto ({self.x},{self.y})"
  def pair (self):
    return (self.x,self.y)

class Linea: 
  def __init__ (self, p1, p2):
    self.p1 = p1
    self.p2 = p2
  def __repr__ (self):
    return (f"Linea ({self.p1.x},{self.p1.y}) "
            f"-- ({self.p2.x},{self.p2.y})")

class Polygono:
  def __init__ (self, ps):
    self.ps = ps
  def __repr__ (self):
    return (f"Polygono ({self.ps})")

out,empty,visited = range (3)

class Board:
  def __init__ (self, cells_x, cells_y ):
    self.cells_x = cells_x
    self.cells_y = cells_y
    self.inner_borders = []
    for i in range (1,self.cells_x):
      for j in range (1,self.cells_y+1):
        self.inner_borders.append (("WE",(i,j),(i+1,j)))
    for j in range (1,self.cells_y):
      for i in range (1,self.cells_x+1):
        self.inner_borders.append (("NS",(i,j),(i,j+1)))  
    self.cells = defaultdict (lambda: out) 
    #self.cells = defaultdict (int) # calls `int ()`, which is 0, which is `out`.
    self.outer_borders = (
      [("N",x,1) for x in range (1,self.cells_x+1)] + 
      [("W",1,y) for y in range (1,self.cells_y+1)] +
      [("E",self.cells_x,y) for y in range (1,self.cells_y+1)] +
      [("S",x,self.cells_y) for x in range (1,self.cells_x+1)] 
    )
    self.start_cell = random.choice (self.outer_borders)
    for i in range (1,cells_x+1):
      for j in range (1,cells_y+1):
        self.cells [i,j] = empty
    self.fluvio = defaultdict (list) # calls `list ()`, which is `[]`.
    self.stack = []
  def visit (self,cell,branca):
    self.cells [cell] = visited
    self.fluvio [branca].append (cell)
    self.stack.append (cell)
  def vicinos (self,cell):
    x,y = cell[-2:]
    vs = [vicino (d1,x,y) for d1 in "NEWS"]
    return [c1 for c1 in vs if self.cells [c1] == empty]
  def way_out (self,cell):
    x,y = cell
    vs = [vicino (d1,x,y) for d1 in "NEWS"]
    return [c1 for c1 in vs if self.cells [c1] == out]

def find_end_cell (board):
  longor = longest_path (board)
  print ("longor = ",longor)
  wout = sorted (
    [(v,k,board.way_out (k)) for k,v in longor.items()
     if board.way_out (k)],
    reverse=True)
  cell_btw = wout[0][1],random.choice(wout[0][2])
  return e_cell (cell_btw),longor,wout[0][0]

def vicino (d,x,y):
  if d == "N": c0 = x,y-1
  if d == "E": c0 = x+1,y
  if d == "W": c0 = x-1,y
  if d == "S": c0 = x,y+1
  return c0

def proximo (d,x,y):
  if d == "N": c0 = "S",x,y-1
  if d == "E": c0 = "W",x+1,y
  if d == "W": c0 = "E",x-1,y
  if d == "S": c0 = "N",x,y+1
  return c0

w_pic, h_pic = 160,160
x_margin,y_margin = 20,20
w_grid,h_grid = w_pic-2*x_margin,h_pic-2*y_margin

tick_w,tick_r = 2,1.5

def draw_sq (pt):
  ct.rectangle (pt.x-tick_r,pt.y-tick_r,2*tick_r,2*tick_r)
  ct.set_source_rgb (0, 0, 0)
  ct.set_line_width (0)
  ct.fill ()

def draw_circle (pt):
  ct.arc (pt.x,pt.y,tick_r,0,tau)
  ct.set_source_rgb (0, 0, 0)
  ct.fill ()

def draw_cross (pt):
  ct.move_to (pt.x-tick_r,pt.y)
  ct.line_to (pt.x+tick_r,pt.y)
  ct.move_to (pt.x,pt.y-tick_r)
  ct.line_to (pt.x,pt.y+tick_r)
  ct.set_source_rgb (0.00, 0.00, 0.00)
  ct.set_line_width (tick_w)
  ct.stroke ()

def draw_point (pt):
  draw_sq (pt)

def draw_rect (p1,p2):
  ct.rectangle (p1.x, p1.y, p2.x - p1.x, p2.y - p1.y)
  
def draw_line (line):
  p1,p2 = line.p1,line.p2
  ct.move_to (p1.x,p1.y)
  ct.line_to (p2.x,p2.y)

def rotated (ps,theta):
  new_ps = []
  for p in ps:
    new_ps.append ((
      p[0]*cos(theta)-p[1]*sin(theta),
      p[0]*sin(theta)+p[1]*cos(theta)))
  return new_ps

def draw_polygono (pg):
  ps = pg.ps
  ct.move_to (ps[0].x,ps[0].y)
  for t in ps[1:]:
    ct.line_to (t.x,t.y)
  ct.close_path ()
  ct.fill ()

def draw_polygon (ps):
  ct.move_to (ps[0].x,ps[0].y)
  for t in ps[1:]:
    ct.line_to (t.x,t.y)
  ct.close_path ()
  ct.set_source_rgb (1, 0.5, 0)
  ct.fill ()

def pairs (pt):
  return (pt.x, pt.y)

def xy (d,x,y):
  return x,y

def create_laby (cells_x,cells_y):
  board = Board (cells_x,cells_y)
  current = board.start_cell
  branca = 0
  board.visit (xy (*current),branca)
  while True:
    while True:
      vics = board.vicinos (current)
      if not vics:
        break
      next_cell = random.choice (vics)
      # print ("next_cell =", next_cell)
      board.visit (next_cell,branca)
      current = next_cell
    branca += 1
    if board.stack:
      current = board.stack.pop ()
      board.fluvio [branca].append (current)
    else:
      break
  board.end_cell,board.longor,board.longest = find_end_cell (board)
  board.word = read_longitude (board.longest)
  return board

def read_longitude (k):
  f = open ("longitudes/longor-" + str (k))
  lns = f.readlines()
  f.close ()
  s = random.choice (lns)
  return s.strip ()

def corner_at (d,x,y):
  if d == "NE": c0 = x,y-1
  if d == "SE": c0 = x,y
  if d == "SW": c0 = x-1,y
  if d == "NW": c0 = x-1,y-1
  if d == "C":  c0 = x-0.5,y-0.5
  return Puncto (
    c0[0] * w_grid/cells_x + x_margin, 
    c0[1] * h_grid/cells_y + y_margin)

def arrow_shape1 ():
  return [
    (0.0,0.025),(0.25,0.025),(0.25,0.1),(0.5,0.0),
    (0.25,-0.1),(0.25,-0.025),(0.0,-0.025)
  ]

def arrow_shape2 ():
  return [
    (0.5,0.025),(0.25,0.025),(0.25,0.1),(0.0,0.0),
    (0.25,-0.1),(0.25,-0.025),(0.5,-0.025)
  ]

def start_arrow (d,x,y,end=False):
  shape = arrow_shape1 () if not end else arrow_shape2 ()
  theta = 0.25 * tau * "ESWN".index (d)
  return Polygono ([Puncto (
    (x1+x-0.5) * w_grid/cells_x + x_margin,
    (y1+y-0.5) * h_grid/cells_y + y_margin
    ) for x1,y1 in rotated (shape,theta)])

"""
def end_arrow (d,x,y):
  theta = 0.25 * tau * "ESWN".index (d)
  return Polygono ([Puncto (
    (x1+x-0.5) * w_grid/cells_x + x_margin,
    (y1+y-0.5) * h_grid/cells_y + y_margin
    ) for x1,y1 in rotated (arrow_shape2 (),theta)])
"""

def ln1 (c1,c2,x,y):
  return Linea (corner_at (c1,x,y), corner_at (c2,x,y))

def create_surface (name):
  filename = name
  if name.endswith (".png"):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)
  if name.endswith (".pdf"):
    surface = cairo.PDFSurface (filename, w_pic, h_pic)
  ct = cairo.Context (surface)
  ct.select_font_face (
    "UnDotum", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
  ct.set_font_size (8)
  ct.rectangle (0, 0, w_pic, h_pic)
  ct.set_source_rgb (1.0, 1.00, 1.00)
  ct.fill()
  return ct,surface

def draw_laby (board):
  #print ("fluvio =",board.fluvio)
  path1 = []
  for branca,fluvio in board.fluvio.items (): 
    path1.append ([(a,b) for a,b in zip (fluvio[0:],fluvio[1:])])
  
  path = []
  for pth in path1:
    for a,b in pth:
      if b < a: 
        a,b = b,a
      x1,y1 = a
      x2,y2 = b
      if x1 < x2:
        brd = "WE"
      if y1 < y2:
        brd = "NS"
      path.append ((brd,a,b))
  
  # print ("inner_borders =", inner_borders)
  # print ("path =", path)
  
  inner_walls = [
    aw for aw in board.inner_borders if aw not in path]
  outer_walls = [
    aw for aw in board.outer_borders 
      if aw not in [board.start_cell,board.end_cell]]
  
  for d,c1,c2 in inner_walls:
    if d == "WE":
      line = ln1 ("NE","SE",*c1)
    if d == "NS":
      line = ln1 ("SW","SE",*c1)
    draw_line (line)
  ct.set_source_rgb (0.00, 0.00, 0.00)
  ct.set_line_width (1.0)
  ct.stroke ()
  
  for d,x,y in outer_walls:
    if d == "N":
      line = ln1 ("NW","NE",x,y)
    if d == "E":
      line = ln1 ("NE","SE",x,y)
    if d == "S":
      line = ln1 ("SE","SW",x,y)
    if d == "W":
      line = ln1 ("SW","NW",x,y)
    draw_line (line)
  ct.set_source_rgb (0.20, 0.20, 0.20)
  ct.set_line_width (1.6)
  ct.stroke ()
   
  pts = [
    corner_at ("NW",i,j)
      for i in range (1,board.cells_x+2) 
        for j in range (1,board.cells_y+2)]

  for p in pts:
    draw_point (p)
  
  sa = start_arrow (*proximo (*board.start_cell))
  ea = start_arrow (*proximo (*board.end_cell),end=True)
  # print (sa)
  ct.set_source_rgb (0.00, 0.00, 0.00)
  draw_polygono (sa)
  draw_polygono (ea)
  print ("longest =",board.longest)
  # paint_longor (board.longor)
  paint_word (board.longor,board.longest,board.word)

def text (ct, string, pos, theta = 0.0, face = 'Sans', font_size = 14):
    ct.save ()
    ct.select_font_face (
      face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ct.set_font_size (font_size)
    fascent, fdescent, fheight, fxadvance, fyadvance = (
      ct.font_extents ())
    x_off, y_off, tw, th = ct.text_extents (string)[:4]
    nx = -tw/2.0
    ny = fheight/2
    ct.translate (pos[0], pos[1])
    ct.rotate (theta)
    ct.translate (nx, ny)
    ct.move_to (0,0)
    ct.show_text (string)
    ct.restore ()

def paint_longor (longor):
  for xy,ln in longor.items():
    p = corner_at ("C",*xy)
    x,y = p.x,p.y
    text (ct, str (ln), pos=(x-0.5,y-2.0), face="UnDotum", font_size=8)

def paint_word (longor,longest,word):
  for xy,ln in longor.items():
    p = corner_at ("C",*xy)
    x,y = p.x,p.y
    text (ct, 
      word [(ln-1) % longest].upper(), pos=(x-0.5,y-2.0), 
      face="UnDotum", font_size=10)

def longest_path (board):
  longor = {}
  ln = 0
  for b,bf in board.fluvio.items():
    for xy in bf:
      if xy not in longor:
        ln += 1
        longor [xy] = ln
      else:
        ln = longor [xy]
  return longor

def e_cell (e_btw):
  cell1,cell2 = e_btw
  x1,y1 = cell1
  x2,y2 = cell2
  if x2 < x1:
    return ("W",x1,y1)
  if x2 > x1:
    return ("E",x1,y1)
  if y2 < y1:
    return ("N",x1,y1)
  if y2 > x1:
    return ("S",x1,y1)


i = 0
# name = f"labyrw/labyrw-{str(i).zfill(5)}.png"
size = 5,5
cells_x,cells_y = size

# name = "labyrw-2.pdf"
# if True:
for i in range (100):
  # name = f"labyrw/labyrw-{str(i).zfill(5)}.pdf"
  name = f"labyrw/labyrw-{str(i).zfill(5)}.png"
  board = create_laby (*size)
  ct,surface = create_surface (name)
  draw_laby (board)

  # print (board.fluvio)
  # print (board.fluvio.keys())

  if name.endswith (".png"):
    surface.write_to_png (name)

