
# python clavaro-tk.py "phrkfzwuybq" "slntvgaioec" "xdmjåöä,.-" # das-fi
# python clavaro-tk.py "qwertyuiop[" "asdfghjkl;'" "zxcvbnm,./" # en-us
# python clavaro-tk.py "qwertyuiopå" "asdfghjklöä" "zxcvbnm,.-" # fi
# clavaro.png 951 x 351 pixels

import argparse
from tkinter import *
from PIL import Image, ImageTk
from numerales import numeral
from math import floor
import random
import time
import sys


def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ('keyorder', nargs='*')
  parser.add_argument ("--timelimit", "-t", type=int, default=0)
  parser.add_argument ("--printresults", "-r", action="store_true")
  parser.add_argument ("--eventinfo", "-e", action="store_true")
  parser.add_argument ("--linear", "-l", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

positions1 = [
  "left-8","left-7","left-6","left-5","left-14",
  "right-14","right-5","right-6","right-7","right-8","right-17",
  "left-4","left-3","left-2","left-1","left-13",
  "right-13","right-1","right-2","right-3","right-4","right-16",
  "left-12","left-11","left-10","left-9","left-15",
  "right-15","right-9","right-10","right-11","right-12"]

# qwerty = "qwertyuiop[" "asdfghjkl;'" "zxcvbnm,./"
qwerty = "qwertyuiopå" "asdfghjklöä" "zxcvbnm,.-"
# qwerty = "phrkfzwuybq" "slntvgaioec" "xdmjåöä,.-"

if args.keyorder:
  qwerty = "".join (args.keyorder)
print ("Key order:", qwerty)

qw = dict (zip (positions1,qwerty))

special = {
  "adiaeresis": "ä",
  "odiaeresis": "ö",
  "aring": "å",
  "bracketleft": "[",
  "apostrophe": "'",
  "semicolon": ";",
  "comma": ",",
  "period": ".",
  "minus": "-",
  "slash": "/",
}

left,right = "left","right"
ia = {"left": "Sinistra","right": "Dextra"}
squares1 = [
  # upper row:
  (left,8,90,60),  
  (left,7,150,60), 
  (left,6,210,60), 
  (left,5,270,60), 
  (left,14,330,60), 
  (right,14,390,60), 
  (right,5,450,60), 
  (right,6,510,60), 
  (right,7,570,60), 
  (right,8,630,60), 
  (right,17,690,60), 
  # middle row:
  (left,4,105,120), 
  (left,3,165,120), 
  (left,2,225,120), 
  (left,1,285,120), 
  (left,13,345,120), 
  (right,13,405,120), 
  (right,1,465,120), 
  (right,2,525,120), 
  (right,3,585,120), 
  (right,4,645,120), 
  (right,16,705,120), 
  # bottom row:
  (left,12,135,180), 
  (left,11,195,180), 
  (left,10,255,180), 
  (left,9,315,180), 
  (left,15,375,180), 
  (right,15,435,180), 
  (right,9,495,180),
  (right,10,555,180),
  (right,11,615,180),
  (right,12,675,180),
]

if args.linear:
  squares = squares1
else:
  squares = []
  for side,num,x,y in squares1:
    for n in range (max (1,13-num)):
      squares.append ((side,num,x,y))

baserow = [
  (left,4,105,120), 
  (left,3,165,120), 
  (left,2,225,120), 
  (left,1,285,120), 
  (right,1,465,120), 
  (right,2,525,120), 
  (right,3,585,120), 
  (right,4,645,120), 
]

file_left,file_right = "results-ia-left.txt","results-ia-right.txt"
w,h = 60,60

def scolor (side):
  if side == right:
    color = "#3771c8"
  else:
    color = "#d40000"
  return color

def res_str (rs):
  if len (rs) == 0:
    t = 0,0,0,0
  else:
    t = [sum (rs[-n:]) / len (rs[-n:]) for n in (1,5,12,1000)]
  return " ".join ([str (len (rs))] + [f"{t1:.3f}"for t1 in t])

def st (t):
  rid1,rid2,side,num = t
  return f"{side}-{num}"

class Window (Frame):
  def __init__(self, root=None):
    self.args = args
    self.results_left = {}
    self.results_right = {}
    self.read_results ()
    Frame.__init__(self, root)
    self.root = root
    image = Image.open ('clavaro.png')
    self.photo = ImageTk.PhotoImage (image)
    canvas = Canvas (root, 
      width=image.size[0], height=image.size[1])
    canvas.create_image (0, 0, anchor=NW, image=self.photo)
    canvas.pack ()
    root.bind("<Escape>", self.on_closing)
    root.bind("<KeyPress>", self.keydown)
    root.protocol("WM_DELETE_WINDOW", self.on_closing)
    self.canvas = canvas
    self.images = [] 
    for side,num,x1,y1 in baserow:
      x,y = x1 + 25, y1 + 25
      if side == right:
        color = "#0000d4"
      else:
        color = "#d40000"
      self.create_rectangle (x,y,x+w,y+h,width=0,fill=color,alpha=0.08)
    self.rects = []
    for side,num,x1,y1 in squares:
      x,y = x1 + 25, y1 + 25
      if side == right:
        color = "#0000d4"
      else:
        color = "#d40000"
      rid1,rid2 = self.create_rectangle (
        x,y,x+w,y+h,width=3,fill=color,alpha=0.50)
      for r in [rid1,rid2]:
        self.canvas.itemconfig (r, state='hidden')
      self.rects.append ((rid1,rid2,side,num))
      self.space = self.create_rectangle (265,266,626,325,width=3)
      self.canvas.itemconfig (self.space, state='hidden')

    self.started = False
    self.rs = []
    self.time = self.canvas.create_text (880,12,font=("sans",12,"bold"),
      text = "00:00")
    self.res = self.canvas.create_text (790,12,font=("sans",12,"bold"),
      text = res_str (self.rs), anchor="e")

    self.tx1 = self.canvas.create_text (350,12,
      text="Press SPACE to start, ESC or [x] to close.")
    text2 = "Keep fingers on the base row. "
    if self.args.timelimit > 0:
      t3 = f"Time limit {self.args.timelimit} minutes."
      text2 += t3 
      print (t3)
    self.tx2 = self.canvas.create_text (475,339,
      text=text2)
    self.spacetx = self.canvas.create_text (445,295, font=("sans",16,"bold"),
      text="")
    self.newkey = None
    self.avgs = 5 * [1000]
    self.gen = self.random_square ()
  def read_results (self):
    rs = [
      (self.results_left,file_left),
      (self.results_right,file_right)]
    for rside,fside in rs:
      try:
        with open (fside) as f:
          print ("Reading", fside)
          lines = f.readlines ()
          for k in lines:
             a,b = k.strip().split(",")
             a,b = int (a), float (b)
             if a in rside:
               rside [a].append (b)
             else:
               rside [a] = [b]
      except:
        pass
    if args.printresults:
      print ("Old results:")
      print ("Left:",self.results_left)
      print ("Right:",self.results_right)
  def sort_results (self):
    for rside in [self.results_left,self.results_right]:
      rside = {k:sorted (v) [:1000] for k,v in sorted (rside.items ())}
  def on_closing (self,e=None):
    self.sort_results ()
    if args.printresults:
      print ("Results:")
      print ("Left:",self.results_left)
      print ("Right:",self.results_right)
      lres = []
      for rside in [self.results_left,self.results_right]:
        lr = sum ([len (v) for k,v in rside.items ()])
        lres.append (lr)
      print ("n = ",sum(lres),lres)
    print ("Results:", res_str (self.rs))
    self.save_results ()
    self.root.destroy ()
  def save_results (self):
    rs = [
      (self.results_left,file_left),
      (self.results_right,file_right)]
    for rside,fside in rs:
      f = open (fside,"w")
      for k,v in rside.items ():
        for x in v:
          f.write (f"{k},{x}\n")
      f.close ()
      print ("Wrote",fside) 
  def random_square (self):
    sqs = self.rects.copy ()
    random.shuffle (sqs)
    while True:
      print ("New sample:","".join ([qw [st (t)] for t in sqs]))
      for x in sqs:
        yield x
      c = len (sqs) // 2 + random.randint (-3,3)
      a,b = sqs [:c], sqs [c:]
      sqs = random.sample (a, len(a)) + random.sample (b, len(b))
  def timeout100 (self):
    now = time.time ()
    time1 = now - self.globaltime
    newtext = (str(floor(time1 / 60)).zfill (2) + ":" + 
      str(floor(time1 % 60)).zfill (2))
    self.canvas.itemconfig (self.time, text=newtext)
    self.root.after (100, self.timeout100)

  def timeout (self):
    if self.newkey:
      rid1,rid2,side,num = self.newkey
      for r in [rid1,rid2]:
        self.canvas.itemconfig (r, state='hidden')
    self.newkey = next (self.gen)
    rid1,rid2,side,num = self.newkey
    self.canvas.itemconfig (self.spacetx,
      text = ia [side] + " " + numeral(num),fill = scolor(side))
    self.canvas.itemconfig (self.space, state='normal')

    self.start = time.time ()
    if self.args.timelimit > 0:
      now = time.time ()
      time1 = now - self.globaltime
      if time1 // 60 >= self.args.timelimit:
        print (f"Time limit reached ({self.args.timelimit} minutes). Quitting.")
        self.on_closing ()
  def keydown (self,e):
    if args.eventinfo:
      print ('down', e, e.char, e.keysym, e.keycode)
    keyname = e.keysym
    if keyname in special:
      keyname = special [keyname]
    if not self.started:
      self.globaltime = time.time ()
      self.canvas.itemconfig (self.tx1, state='hidden')
      self.canvas.itemconfig (self.tx2, state='hidden')
      print ("Started.")
      self.started = True
      self.root.after (1000, self.timeout)
      self.root.after (100, self.timeout100)
    else:
      if self.newkey:
        self.accept_key (keyname,self.newkey)
  def accept_key (self,keyname,newkey):
    rid1,rid2,side,num = newkey
    kb = st (newkey)
    if keyname == qw [kb]:
      self.end = time.time ()
      for r in [rid1,rid2]:
        self.canvas.itemconfig (r, state='normal')
      print ("Correct:", keyname)
      total = self.end - self.start
      total = round (float (total), 4)
      self.avgs = self.avgs[-4:] + [1000 * total]
      print (qw [kb], total)
      if side == left:
        if num in self.results_left:
          self.results_left [num].append (total)
        else:
          self.results_left [num] = [total]
      if side == right:
        if num in self.results_right:
          self.results_right [num].append (total)
        else:
          self.results_right [num] = [total]

      self.canvas.itemconfig (self.spacetx, text="")
      self.canvas.itemconfig (self.space, state='hidden')
      # self.newkey = None
      avg = round (0.6 * sum (self.avgs) / len (self.avgs))
      avg = min (avg,2000)
      self.root.after (avg, self.timeout)
      self.rs.append (total)
      self.canvas.itemconfig (self.res, text=res_str (self.rs))
    else:
      print ("Wrong:", keyname)
  def create_rectangle (self,x1, y1, x2, y2, **kwargs):
    id1 = None
    if 'alpha' in kwargs:
      alpha = int(kwargs.pop('alpha') * 255)
      fill = kwargs.pop('fill')
      fill = root.winfo_rgb(fill) + (alpha,)
      image = Image.new('RGBA', (x2-x1, y2-y1), fill)
      self.images.append(ImageTk.PhotoImage(image))
      id1 = self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
    id2 = self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    return (id1,id2)

root = Tk ()
win = Window (root)
root.title ('Clavaro-ia')
win.mainloop()

