
# python scatter-scores-1.py --days --fit --degree 2 --color "#060606" --before "2023-01-25 20:20:20" --ylabel "Parolas per minuta" --xlabel "Dies" --title ""


import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt
import json
import datetime as dt
import numpy as np
import argparse
import random
import matplotlib.font_manager as fm
from pylab import rcParams

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("--after", type=str, default="0000-00-00 00:00")
  pad ("--before", type=str, default="9999-99-99 99:99")
  pad ("--time", action="store_true")
  pad ("--days", action="store_true")
  pad ("--tinytt", action="store_true")
  pad ("--fit", action="store_true")
  pad ("--degree", type=int,default=3)
  pad ("--title", default=
    'My Touch Typing Exercises (Since September 2022)')
  pad ("--ylabel", default='words per minute')
  pad ("--xlabel", default='days')
  pad ("--color", default='#3182ce')
  pad ("--linewidth", type=float, default=3)
  args = parser.parse_args ()
  return (args)

args = read_args()

def wpm (cpm):
  return cpm / 5.0
# findfont: Font family ['Another Typewriter'] not found. Falling back to DejaVu Sans.
# then:
# rm ~/.cache/matplotlib -fr
if args.tinytt:
  fp = fm.FontProperties(fname='/usr/share/fonts/opentype/another/Another_Typewriter_Regular.ttf')
  rcParams['font.family'] = fp.get_name()
  #fig, ax = plt.subplots(figsize=(2, 2))
  fig = plt.figure(figsize=(2, 2))
  plt.rcParams["figure.figsize"] = (2,2)
  rcParams['figure.figsize'] = 2, 2
  #fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(2.8, 2.8, forward=True)
  fig.subplots_adjust(bottom=0.2)
  fig = plt.figure(1)
  ax = fig.add_subplot(111)
  #handles, labels = ax.get_legend_handles_labels()
  #lgd = ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5,-0.1))
  #fig.savefig('samplefigure', bbox_extra_artists=(lgd,), bbox_inches='tight')
  # plt.tight_layout()
fig = plt.figure(1)
ax = fig.add_subplot(111)
# This does not work:
# matplotlib.rcParams['font.sans-serif'] = "Another Typewriter"
# Then, "ALWAYS use sans-serif fonts"
# matplotlib.rcParams['font.family'] = "sans-serif"
f = open ("scores.txt")
s = f.read ()
f.close ()
t = [x.split("\t") for x in s.split("\n")]
scores = [(float(a),b,float(c)) for a,b,c in t]
table = scores
table1 = table[:]
table.sort (key=lambda x: x[1])
table = [[score,d] for score,d,errs in table if score > 30 and args.after <= d <= args.before]
print ("Number of scores =",len(table))
print ("Best scores:")
for x,t,e in table1[:30]:
  print (f"{x:>7.1f} {t} {e:>5.2f}")
plt.xlabel('experimentos')
yAxis = [score for score,d in table]
#plt.yticks (np.arange(35, 71, 5))
#plt.xticks (np.arange(0, 151, 30))
if args.time:
  xAxis = [dt.datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for score,d in table]
elif args.days:
  ds = [dt.datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for score,d in table]
  ds1 = min (ds)
  aval = list(set([(d1-ds1).days for d1 in ds]))
  print (aval)
  #xAxis = [(d1-ds1).days + random.random() for d1 in ds]
  xAxis = [aval.index((d1-ds1).days) + random.random() for d1 in ds]
  plt.xlabel (args.xlabel)
else:
  xAxis = [t for t,x in enumerate (table)]

"""
for i in range (1,500):
  yAxis.insert (0,30-random.random()*20)
  xAxis.insert (0,0-random.random ())
"""

if args.fit:
  list_x = xAxis 
  list_y = yAxis 
  poly = np.polyfit(list_x,list_y,args.degree)
  poly_y = np.poly1d(poly)(list_x)
  ax.plot (list_x,poly_y,linewidth=args.linewidth,c=args.color, solid_capstyle='round')
else:
  plt.scatter (xAxis,yAxis,s=5,c=args.color)

# plt.ylabel('parolas per minuta')
plt.ylabel (args.ylabel)
plt.title (args.title)
if args.fit:
  figname = 'scatter-scores-fitted.pdf'
else:
  figname = 'scatter-scores.pdf'
plt.savefig (figname, bbox_inches='tight')  
plt.show ()

