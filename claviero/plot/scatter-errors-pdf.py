import matplotlib.pyplot as plt
import json
import datetime as dt
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ("--time", action="store_true")
  pad ("-o", "--outpic", default="scatter-errors-1.pdf")
  args = parser.parse_args ()
  return (args)

args = read_args()

table = json.load(open('errors.json', 'r'))
table.reverse ()
table1 = table[:]
table1.sort (key=lambda x: x[0])
table = [[ers,d] for ers,d in table]
print ("Number of experimentos =",len(table1))
print ("Latests:")
for x,t in table1[:30]:
  print (f"{x:>7.2f} {t}")
xAxis = [t for t,x in enumerate (table)]
yAxis = [ers for ers,d in table]

fig, ax = plt.subplots(figsize=(5, 3))
plt.scatter (xAxis,yAxis,s=5,color="k")

plt.ylabel('errors percent')
plt.xlabel('experimentos')
fig.tight_layout()

# plt.show()
plt.savefig(args.outpic)  
print ("Scribeva", args.outpic)
