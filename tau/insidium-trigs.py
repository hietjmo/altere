#!/usr/bin/python

# python cairo-test-strs.py

import os
import shutil
import cairo
import numpy as np
from math import *
# import k

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
bg_gris = (0.96,0.96,0.96)
bg_blanc = (1.00, 1.00, 1.00)
fg_nigre = (0.00, 0.00, 0.00)

colores = [
  ("0",gris),("1",blau_obscur),("2",violet),("3",blau),
  ("4",blau_clar),("5",verde_obscur),("6",verde_clar),
  ("7",jalne),("8",orange),("9",rubie),(".",brun)]

colordict = dict (colores)

w_pic, h_pic = 1280,720
center_x, center_y = w_pic/2, h_pic/2

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)


def draw_circle (x,y,r):
  ct.arc (x,y,r,0,tau)
  ct.stroke ()

def draw_cross (x,y,tick_r):
  ct.move_to (x-tick_r, y-tick_r)
  ct.line_to (x+tick_r, y+tick_r)
  ct.move_to (x-tick_r, y+tick_r)
  ct.line_to (x+tick_r, y-tick_r)
  ct.stroke ()

def draw_sexa (x,y,r):
  puntos = []
  for d in np.arange (0,tau,tau/6):
    x1 = x + r * cos (d)
    y1 = y - r * sin (d)
    puntos.append ((x1,y1))
  for x1,y1 in puntos:
    ct.move_to (x,y)
    ct.line_to (x1,y1)
  for x1,y1 in puntos:
    ct.line_to (x1,y1)
  ct.stroke ()
  return puntos

def surface_write_to_png (filename,save=True):
  if save:
    surface.write_to_png (filename)
  print (F"file '{filename}'")
  print ("duration 0.25")

def phase_2 (puntos,bn):
  #bn =  F'{i:06b}'
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.new_path ()

  #bn =  F'{i:06b}'
  cnt = bn.count ('1')
  for k,c in enumerate (bn):
    if c == '1':
      ct.move_to (center_x, center_y)
      ct.line_to (*puntos[k])
      kk = (k+1) % len (puntos)
      ct.line_to (*puntos[kk])
      ct.close_path ()
      ct.set_source_rgb (*colordict[str(cnt)])
      ct.fill ()

  ct.set_source_rgb (*fg_nigre)
  ct.set_line_width (3.0)
  draw_sexa (center_x, center_y, 300)
  ct.set_line_width (5.0)
  draw_circle (center_x, center_y, 300)
  surface_write_to_png (F"sexa/pic-2-{bn}.png")
  return (F"sexa/pic-2-{bn}.png")

def phase_1 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  ct.new_path ()
  ct.set_source_rgb (*fg_nigre)
  ct.set_line_width (5.0)
  draw_circle (center_x, center_y, 300)
  ct.set_line_width (3.0)
  # draw_cross (center_x, center_y, 5)
  puntos = draw_sexa (center_x, center_y, 300)
  surface_write_to_png ("sexa/pic-1.png")
  return (puntos)

def phase_0 ():
  ct.set_source_rgb (*bg_gris)
  ct.paint ()
  surface_write_to_png ("sexa/pic-0.png")

crear ("sexa")
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w_pic, h_pic)
ct = cairo.Context (surface)
phase_0 ()
puntos = phase_1 ()

ef01234567 = [
  '000000', '001000', '000100', '000010', '000001', '100000', 
  '010000', '110000', '101000', '011000', '001100', '001010', 
  '000110', '000101', '001001', '010010', '010100', '100100', 
  '100010', '000011', '100001', '010001', '011001', '011010', 
  '011100', '001110', '010110', '000111', '010011', '100011', 
  '100101', '010101', '110100', '110010', '100110', '001101', 
  '001011', '101010', '101100', '111000', '101001', '110001', 
  '111100', '011101', '101101', '011011', '110011', '110101', 
  '111001', '111010', '110110', '101110', '011110', '001111', 
  '010111', '100111', '101011', '111011', '110111', '101111', 
  '011111', '111110', '111101', '111111', ]
# ti = k.t5f24ad13 
# ti = k.tced146a0
# ti = k.ef01234567
ti = ef01234567

for i in ti:
  lastfile = phase_2 (puntos,i)

print (F"file '{lastfile}'")



