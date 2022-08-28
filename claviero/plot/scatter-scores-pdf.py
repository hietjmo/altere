import matplotlib.pyplot as plt
import json
import datetime as dt
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("--time", action="store_true")
  pad ("-o", "--outpic", default="scatter-scores-1.pdf")
  args = parser.parse_args ()
  return (args)

args = read_args()

def wpm (cpm):
  return cpm / 5.0

table = json.load(open('scores.json', 'r'))
table1 = table[:]
table.sort (key=lambda x: x[1])
table = [[wpm(score),d] for score,d in table if score > 50]
print ("Number of scores =",len(table))
print ("Best scores:")
for x,t in table1[:30]:
  print (f"{wpm(x):>7.1f} {t}")
yAxis = [score for score,d in table]
if args.time:
  xAxis = [dt.datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for score,d in table]
else:
  xAxis = [t for t,x in enumerate (table)]

fig, ax = plt.subplots(figsize=(5, 3))
plt.scatter(xAxis,yAxis,s=5)

plt.ylabel('parolas per minuta')
plt.xlabel('experimentos')
fig.tight_layout()

# plt.show()
plt.savefig(args.outpic)  
print ("Scribeva", args.outpic)
