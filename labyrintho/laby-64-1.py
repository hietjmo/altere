
import os
import time
import random

abc = (
  "ABCDEFGH"  
  "JKLMNPQR"
  "STUVWXYZ"
  "abcdefgh"
  "jklmnpqr"
  "stuvwxyz"
  "αβγδεζηθ"
  "ικλμνξπρ"
)

def vicino (d,x,y):
  if d == "N": c0 = x,y-1
  if d == "E": c0 = x+1,y
  if d == "S": c0 = x,y+1
  if d == "W": c0 = x-1,y
  return c0

def vicinos (c):
  x,y = pos (c)
  vs = [vicino (d1,x,y) for d1 in "NESW"]
  return [letter (x,y) for (x,y) in vs 
    if 0 <= x < 8 and 0 <= y < 8]

def letter (x,y):
  return abc [8*y+x]

def pos (c):
  x = abc.index (c)
  y,x = divmod (x,8)
  return x,y

vicin_dict = {c:vicinos(c) for c in abc}

print ("\n".join (abc [8*y:8*(y+1)] for y in range(8)))
print (vicin_dict)

border = "ABCDEFGHRZhrzθικλμνξπραsjaSJ"
fullabys = "fullabys-2.txt"
i = 0
ts = 0.000

f = open (fullabys,"a")
t1 = time.time()
while True:
  path = random.choice (border)
  d = [e for e in vicin_dict [path[-1]]]
  c = random.choice (d)
  while d:
    path = path + c
    d = [e for e in vicin_dict [path[-1]] if e not in path]
    if d: c = random.choice (d)
  if len (path) == 64 and path[-1] in border:
    t2 = time.time()
    t = t2 - t1
    t1 = t2
    i = i + 1
    ts = ((i-1)*ts + t) / i
    print (F"{t:9.3f} {ts:4.1f} {path} {i}")
    f.write (path + "\n")
    f.flush ()



