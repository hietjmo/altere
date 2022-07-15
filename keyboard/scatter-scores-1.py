import matplotlib.pyplot as plt
import json
import datetime as dt


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

plt.tight_layout()
plt.scatter(xAxis,yAxis,s=5)

plt.ylabel('claves per minuta')
plt.xlabel('experimentos')

plt.show()
