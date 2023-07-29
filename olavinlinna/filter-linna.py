
# python filter-linna.py > olavinlinna-1.txt

"""
p1: N=6860540.048, E=599901.000
p2: N=6860425.298, E=600090.500
599999.73 6858002.07 76.81
599999.74 6858005.88 76.86
"""

class point():
  pass

p1 = point()
p2 = point()

p1.x = 599901.000
p1.y = 6860540.048
p2.x = 600090.500
p2.y = 6860425.298

f = open ("N5311A3.txt")
for s in f:
  x,y,z = map (float, s.strip().split(" "))
  if p1.x < x < p2.x and p1.y > y > p2.y:
    print (F"{x:.2f} {y:.2f} {z:.2f}")

f.close ()
