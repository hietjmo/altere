import matplotlib.pyplot as plt
import json
import datetime as dt
import numpy as np
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-deg", "--degree", type=int, default=5)
  args = parser.parse_args ()
  return (args)

args = read_args()

class reversor:
  def __init__(self, obj):
    self.obj = obj
  def __eq__(self, other):
    return other.obj == self.obj
  def __lt__(self, other):
    return other.obj < self.obj

table = json.load(open('scores.json', 'r'))
table1 = table[:]
table.sort (key=lambda x: x[1])
# xAxis = [dt.datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for score,d in table]
table = [[score,d] for score,d in table if score > 50]
print ("Number of scores =",len(table))
print ("Best scores:")
for x,t in table1[:30]:
  print (f"{x:>7.1f} {t}")
xAxis = [t for t,x in enumerate (table)]
yAxis = [score for score,d in table]
# plt.grid(True)
list_x = xAxis 
list_y = yAxis 
poly = np.polyfit(list_x,list_y,args.degree)
poly_y = np.poly1d(poly)(list_x)
plt.plot(list_x,poly_y)


# plt.plot(xAxis,yAxis)

plt.ylabel('claves per minuta')
plt.xlabel('experimentos')

plt.show()
