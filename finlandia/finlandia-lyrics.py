#!/usr/bin/python3

from PIL import Image,ImageDraw,ImageFont
import argparse
import shutil
import os
import re

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("--font", default="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
  pad ("--fontsize", default=34)
  args = parser.parse_args ()
  return args

args = read_args ()

sw,sh = 320,240
white = "#fafafa"
blue = "#124281"

def hex_to_rgb (hex):
  h = hex.lstrip('#')
  return tuple (int (h[i:i+2], 16)  for i in (0, 2, 4))

finlandia = """
Oi, Suomi, katso, sinun päiväs' koittaa,
yön uhka karkoitettu on jo pois,
ja aamun kiuru kirkkaudessa soittaa,
kuin itse taivahan kansi sois'.
Yön vallat aamun valkeus jo voittaa,
sun päiväs' koittaa, oi synnyinmaa.

Oi, nouse, Suomi, nosta korkealle,
pääs' seppelöimä suurten muistojen.
Oi, nouse, Suomi, näytit maailmalle,
sa että karkoitit orjuuden,
ja ettet taipunut sa sorron alle,
on aamus' alkanut, synnyinmaa.
""" # Veikko Antero Koskenniemi, 1940

dirpath = "pngs"
if os.path.exists (dirpath) and os.path.isdir (dirpath):
  shutil.rmtree (dirpath)
os.mkdir (dirpath)
flagfile = "flagmorph"
shutil.copyfile (F"{flagfile}.png", F"{dirpath}/{flagfile}.png")
im = Image.new (mode="RGB", size=(sw,sh))
draw = ImageDraw.Draw (im)
font = ImageFont.truetype (args.font, args.fontsize)

formants = {
  " ": 0,
  "i": 321,
  "e": 443,
  "ä": 600,
  "y": 330,
  "ö": 436,
  "a": 609,
  "o": 433,
  "u": 332,
} # Iivonen, p. 31

print (formants.keys())

finlandia2 = finlandia.replace ("\n","  ")
vows = [c for c in finlandia2 if c.lower() in formants]

print ("vows =",vows)

words0 = re.split (r'\W+', finlandia.strip())
words1 = [w for w in words0 if w != ""]
print ("words1 =",words1)
print ()

d = []
i = 0
for w in words1:
  while i < len(vows) and vows [i] == ' ':
    d.append ((" ","space"))
    i = i + 1
  while i < len(vows) and vows [i] in w:
    d.append ((vows [i],w))
    i = i + 1

print ("d =", d)
x1,y1 = sw/2,sh/2
maxsize = 0,""

for w in set (words1):
  im.paste (hex_to_rgb (white), [0,0,im.size[0],im.size[1]])
  draw.text ((x1,y1), w, fill=hex_to_rgb (blue), font=font, anchor="mm")
  left, top, right, bottom = font.getbbox (w)
  size_x = right - left
  if size_x > maxsize[0]:
    maxsize = size_x,w
  filename = F"{dirpath}/{w}.png"
  im.save (filename)
  print (filename)

im.paste(hex_to_rgb (white), [0,0,im.size[0],im.size[1]])
filename = dirpath + F"/space.png"
im.save (filename)
print (filename)
print ("maxsize =",maxsize)
mylist = "mylist.txt"
f = open (mylist,"w")
for a,b in d:
  f.write (F"file '{dirpath}/{b}.png'\n")
  f.write (F"duration 0.25\n")

flagfile = "flagmorph"
path = F"{flagfile}.png"
im1 = Image.new (mode="RGBA", size=(sw,sh))
draw = ImageDraw.Draw (im1)
im1.paste (hex_to_rgb (white), [0,0,im1.size[0],im1.size[1]])
im2 = Image.open(path).convert("RGBA")

for a in range (101):
  alpha = a/100
  im3 = Image.blend (im1, im2, alpha)
  filename = F"{dirpath}/blended-{a}.png"
  im3.save (filename)
  f.write (F"file '{filename}'\n")
  f.write (F"duration 0.04\n")

f.write (F"file '{dirpath}/{flagfile}.png'\n")
f.write (F"duration 1.00\n")
f.write (F"file '{dirpath}/{flagfile}.png'\n")

print ("Wrote", mylist)

# ffmpeg -y -f concat -safe 0 -i mylist.txt -c:v libx264 -pix_fmt yuv420p video.mp4
## ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac output.mp4
# ffmpeg -y -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
## ffmpeg -i audio.wav -i video.mp4 -acodec copy -vcodec copy -f mkv output.mkv

