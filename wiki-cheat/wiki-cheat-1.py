#!/usr/bin/python

from fpdf import FPDF
import textwrap
import string
import cairo

file1 = "Corpora_IA_Wiki_4000_IA.txt"
file2 = "Corpora_IA_Wiki_4000_EN-v2.txt"

def flatten (t):
  return [item for sublist in t for item in sublist]

def create_surface (filename):
  # w_pic, h_pic = 1748,2480 # 300 dpi
  w_pic, h_pic = 874, 1240 # 150 dpi
  if filename.endswith (".png"):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)
  if filename.endswith (".pdf"):
    surface = cairo.PDFSurface (filename, w_pic, h_pic)
  ct = cairo.Context (surface)
  ct.select_font_face (
    "Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
  ct.set_font_size (24)
  ct.rectangle (0, 0, w_pic, h_pic)
  ct.set_source_rgb (1.00, 1.00, 1.00)
  ct.fill()
  return ct,surface

printable = set (string.printable)

def modify (text):
  result = []
  for ln in text:
    ln1 = ln.strip()
    ln1 = ''.join (filter (lambda x: x in printable, ln1))
    ln1 = textwrap.wrap (ln1, 65)
    result.extend (ln1)
  return result

f = open (file1)
text1 = f.readlines (3000)
f.close ()

f = open (file2)
text2 = f.readlines (3000)
f.close ()

text1 = modify (text1)
text2 = modify (text2)

text1 = text1 [:45]
text2 = text2 [:45]

imgname = "page.png"
ct, surface = create_surface ("page.png")
ct.set_source_rgb (0.00, 0.00, 0.00)
for i,t in enumerate (text1):
  ct.move_to (10, 26*(i+1))
  ct.show_text (t)

if imgname.endswith (".png"):
  surface.write_to_png (imgname)

pdf = FPDF('P', 'mm', 'A5')

pdf.add_page ()
pdf.image ('page.png', x=0, y=0, w=148, h=210)
pdf.set_font ('Arial', '', 0.01)
pdf.set_text_color (210,210,210)
pdf.set_xy (0,0)
for i,t in enumerate (text2):
  pdf.cell (0,0,txt=t,ln=1)
pdf.output ('wiki-cheat.pdf', 'F')

# print (text1)
# print (text2)


