
import matplotlib.pyplot as plt
import cartopy.crs as cr
import cartopy.feature as cf

def unique (xs):
  return list (set (xs))

filename = "constellationship.fab"
f = open (filename)
lines = f.readlines ()
f.close ()

s1 = [s.strip().split() for s in lines if len(s)>5]
s2 = {x[0]:[int(a) for a in x[2:]] for x in s1}

filename = "hip_cons_692.txt"
f = open (filename)
lines = f.readlines ()
f.close ()

xs = [s.strip().split() for s in lines]
d = {}
for x in xs:
  hipnum = int (x[0])
  ra  = float (x[1])
  dec = float (x[2])
  mag = float (x[3])
  d [hipnum] = ra,dec,mag

starnums1 = unique (s2['UMa'])
stars1 = [d[st] for st in starnums1]
print (stars1)

lat,lon = [],[]
for x,y,r in stars1:
  lon.append (x)
  lat.append (y)

avg_lon = sum (lon) / len (lon)
avg_lat = sum (lat) / len (lat)

plt.figure (figsize=(10,10))
proj = cr.Orthographic(central_latitude=avg_lat,central_longitude=avg_lon)
ax = plt.axes (projection=proj)
ax.set_global()
ax.add_feature (cf.COASTLINE)
plt.scatter(lon, lat, transform=cr.PlateCarree())
plt.show() 


