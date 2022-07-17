
from collections import defaultdict

ordine = 'EAION STRLU CDPMV BGHFQ XJYKZ W'
ordine1 = ordine.lower().replace(" ","")

f = open ("resultlog.txt")
r,r1 = [],[]
for line in f:
  a,b = line.rstrip().split (" ")
  if ('a' <= a <= 'z'):
    r1.append ((a,float (b)))
  else:
    if r1:
      r.append (sorted (r1,key=lambda x: x[1]))
    r1 = []
    
result = []
for x,r1 in enumerate (r):
  for y,c in enumerate (r1):
    result.append ((y,x,c[0],c[1]))
     
max_x = 0
for y,x,c,d in result:
  max_x = max (x,max_x)

result.sort()
ln = ""
old_y = 0
for y,x,c,d in result:
  if y != old_y:
    ln += "\n"
  if x == 0:
    ln += f" {d:.4f}"
  ln += f" {c}"
  if x == max_x:
    ln += f" {d:.4f}"
    dy = ordine1.index (c) - y
    ln += f" {dy:+3d}"
    ln += f" {ordine1[y]}"


  old_y = y

print (ordine)
print (ln)

