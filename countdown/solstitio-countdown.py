

# python countdown-2.py --countten --render
# ffmpeg -y -framerate 20 -pattern_type glob -i 'render/*.png' -c:v libx264 -pix_fmt yuv420p anim-1.mp4

import pygame
import calendar, time
import os
import shutil
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("-t", "--text", default="BON SOLSTITIO!")
  pad ("-s", "--shifted", default="")
  pad ("--countten", action="store_true")
  pad ("--nogreet", action="store_true")
  pad ("--render", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

openmojipalette = {
  'blue': '#92d3f5', 'blueshadow': '#61b2e4', 'red': '#ea5a47',
  'redshadow': '#d22f27', 'green': '#b1cc33', 'greenshadow': '#5c9e31',
  'yellow': '#fcea2b', 'yellowshadow': '#f1b31c', 'white': '#ffffff',
  'lightgrey': '#d0cfce', 'grey': '#9b9b9a', 'darkgrey': '#3f3f3f',
  'bggrey': '#333333', 'black': '#000000', 'orange': '#f4aa41',
  'orangeshadow': '#e27022', 'pink': '#ffa7c0', 'pinkshadow': '#e67a94',
  'purple': '#b399c8', 'purpleshadow': '#8967aa', 'brown': '#a57939',
  'brownshadow': '#6a462f', 'LightSkinTone': '#fadcbc',
  'MediumLightSkinTone': '#debb90', 'MediumSkinTone': '#c19a65',
  'MediumDarkSkinTone': '#a57939', 'DarkSkinTone': '#6a462f',
  'DarkSkinShadow': '#352318', 'NavyBlue': '#1e50a0',
  'Maroon': '#781e32', 'DarkGreen': '#186648'}

def hex_to_rgb (hex):
  h = hex.lstrip ('#')
  return tuple (int (h[i:i+2], 16) for i in (0, 2, 4))

def om (name,alpha=255):
  return hex_to_rgb (openmojipalette [name]) + (alpha,)

intervals = (
  ('d', 86400),   # 60 * 60 * 24
  ('h', 3600),    # 60 * 60
  ('min', 60),
  ('s', 1),
)

def days_hours_mins (seconds):
  seconds = round (seconds)
  result = []
  for name, count in intervals:
    value = seconds // count
    seconds = seconds - value * count
    result.append (value)
  return result

def seconds_epoch (t):
  return calendar.timegm (time.strptime (t,'%Y-%m-%d %H:%M:%S'))

def diff_str (delta):
  sign = 1 if delta >= 0 else -1
  days,hours,mins,sec = days_hours_mins (abs(delta))
  pm = "+" if sign == 1 else "-"
  return delta,f"{pm}{days:03} {hours:02} {mins:02} {sec:02}"


size = 680,180

dirpath = "render"
if os.path.exists (dirpath) and os.path.isdir (dirpath):
  shutil.rmtree (dirpath)
if args.render:
  os.mkdir (dirpath)

f = open ("eqnox-gmt-list.txt")
xs = f.readlines ()
f.close ()

wss = [s.strip () for s in xs if s[0:2] == "WS"]
thens = [calendar.timegm (time.strptime (t,'WS %Y-%m-%d %H:%M')) for t in wss]

pygame.init ()
screen = pygame.display.set_mode (size)
fontname = "fonts/jd_lcd_rounded.ttf"
font = pygame.font.Font (fontname,100)
image = pygame.Surface(size, pygame.SRCALPHA)
clock = pygame.time.Clock ()
running = True
if args.countten:
  args.shifted = "2024-12-21 09:19:40"
if args.shifted:
  time1 = time.time ()
  time2 = calendar.timegm (time.strptime (args.shifted,'%Y-%m-%d %H:%M:%S'))
color = om ("yellow")
frame = 0

while running:
  image.fill (om ("bggrey"))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  now = time.time ()
  if args.shifted:
    now = now - time1 + time2
  deltas = [now-then for then in thens]
  absdeltas = [abs (now-then) for then in thens]
  minindex = absdeltas.index (min (absdeltas))
  minitem = deltas [minindex]
  delta,text = diff_str (minitem)
  if -0.5 <= delta <= 1.5 and not args.nogreet:
    text = args.text
  img = font.render (text,True,color)
  rect = img.get_rect (center = (size[0]/2,size[1]/2))
  image.blit (img, rect)
  screen.blit (image, (0,0))
  if args.render:
    pygame.image.save (image,f"render/frame{frame:04}.png")
    frame = frame + 1
  pygame.display.update ()
  clock.tick (20)

"""
time.gmtime ([secs])
seconds -> struct_time in UTC

time.localtime ([secs])
seconds -> struct_time in local time

time.mktime (t)
struct_time -> seconds

time.strftime (format[, t])
tuple or struct_time -> string

time.strptime (string[, format])
string -> struct_time

time.time ()
-> seconds

calendar.timegm (tuple)
tuple -> seconds

The time.gmtime () and calendar.timegm () are each others’ inverses.
The time.localtime () and time.mktime () are each others’ inverses.
"""
