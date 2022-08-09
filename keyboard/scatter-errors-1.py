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

table = json.load(open('errors.json', 'r'))
table.reverse ()
table1 = table[:]
table1.sort (key=lambda x: x[0])
# xAxis = [dt.datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for score,d in table]
table = [[ers,d] for ers,d in table]
print ("Number of experimentos =",len(table1))
print ("Best scores:")
for x,t in table1[:30]:
  print (f"{x:>7.2f} {t}")
xAxis = [t for t,x in enumerate (table)]
yAxis = [ers for ers,d in table]
# plt.grid(True)

plt.tight_layout()
plt.scatter(xAxis,yAxis,s=5,color="k")

plt.ylabel('errors percent')
plt.xlabel('experimentos')

plt.show()
