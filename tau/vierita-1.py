import os
import shutil
from numeraalit import numeraali
from PIL import Image, ImageDraw
import argparse

# python vierita-1.py -d dir1/anim-png -i 45
# ffmpeg -y -i dir1/anim-png/tau/anim-png/%07d.png -c:v libx264 -r 25 -pix_fmt yuv420p kuusi-piste-kaksi-kahdeksan.mp4

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ("-n", "--number", type=int, default=0)
  parser.add_argument ("-i", "--items", type=int, default=0)
  parser.add_argument ("-s", "--srcpath", default="pics")
  parser.add_argument ("-d", "--destpath", default="anim-png")
  parser.add_argument ("--debug", action="store_true")
  parser.add_argument ("--log", action="store_true")
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
for i,c in enumerate (tau_list):
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

dit = {}
n = 1
for x in t[2:]:
  k = len (x)
  inpic = 'numero-' + numeraali (int(x)) + '.png'
  dit [inpic] = " ".join ([str (z) for z in range (n,k+n)])
  n += k

print (dit)

destpath = args.destpath
srcpath = args.srcpath
if os.path.exists (destpath) and os.path.isdir (destpath):
  shutil.rmtree (destpath)
os.mkdir (destpath)

step = 5

ws = []
start = 0

pics = []
pics.append ("insidium-720.png")
pics.append ("insidium-sex.png")
for instr in t:
  if instr == ".":
    numstr = "piste"
  else:
    numero = int (instr)
    text = str (numero)
    numstr = numeraali (numero)
  
  numtext = numstr + "."
  
  inpic = 'numero-' + numstr + '.png'
  pics.append (inpic)
  pics.append ("empty-cent.png")

selection = pics

for name in selection:
  src = srcpath + "/" + name
  im = Image.open (src)
  width, height = im.size
  end = start + width - 1
  ws.append ((im,name,start,end,width,height))
  start = start + width

print (len (range (-360,end-920,step)))

for frame,x in enumerate (range (-360,end-360,step)):
  img = Image.new ('RGB', size=(1280, 720), color='#fee0c2')
  names = []
  for im,name,s,e,w,h in ws:
    if s <= x <= e or x <= s <= x + 1280:
      img.paste (im, (s-x,0))
      if name in dit:
        names.append ("Desimaalit: " + dit [name])
    draw = ImageDraw.Draw (img)
    for i,nom in enumerate (names):
      draw.text((3, i*10+2), nom, fill='black')
  img.save (destpath + "/" + str(frame).zfill (7) + '.png')
  if frame % 100 == 0:
   print (frame,names)

