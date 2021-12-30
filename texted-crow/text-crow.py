
from PIL import Image, ImageDraw, ImageFont

im = Image.open ('crow.png') 
pix = im.load ()
sizex,sizey = im.size
f = open ("blacky-the-crow.txt")
text = f.read ()
f.close ()

text = text.replace ("\n"," ")

def blacky ():
  for c in text:
    yield c

chars = {}
image = Image.new ("RGB", (sizex,sizey), "white")
draw = ImageDraw.Draw (image)
font = ImageFont.truetype ("FreeMonoBold.ttf", 12)
gen = blacky ()
w, h = draw.textsize ("X", font=font)
print (w,h)
for y in range (0,sizey-h,h):
  s = ""
  for x in range (0,sizex-w,w):
    pts = []
    for y1 in range (0,h):
      for x1 in range (0,w):
        r,g,b,a = pix [x+x1,y+y1]
        pts.append ((r+g+b)//3)
    avg = sum (pts) // len (pts)
    if avg < 128:
      s += next (gen)
    else:
      s += " "
  draw.text ((0,y), s, font=font, fill=(0,0,0))
  print (s)

image.save ('texted-crow.png') 

