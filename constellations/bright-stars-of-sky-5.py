
import matplotlib.pyplot as plt
import cartopy.crs as cr
import cartopy.feature as cf
import argparse

"""
And Ant Aps Aqr Aql Ara Ari Aur Boo Cae Cam Cnc CVn CMa CMi Cap Car Cas Cen Cep Cet Cha Cir Col Com CrA CrB Crv Crt Cru Cyg Del Dor Dra Equ Eri For Gem Gru Her Hor Hya Hyi Ind Lac Leo LMi Lep Lib Lup Lyn Lyr Men Mic Mon Mus Nor Oct Oph Ori Pav Peg Per Phe Pic Psc PsA Pup Pyx Ret Sge Sgr Sco Scl Sct Ser Sex Tau Tel Tri TrA Tuc UMa UMi Vel Vir Vol Vul
"""

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-wx", "--width", type=int, default=1280)
  pad ("-hy", "--height", type=int, default=720)
  pad ("-d", "--folder", default=".")
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()


def unique (xs):
  return list (set (xs))

filename = "constellationship.fab"
f = open (filename)
lines = f.readlines ()
f.close ()

s1 = [s.strip().split() for s in lines if len(s)>5]
s2 = {x[0]:[int(a) for a in x[2:]] for x in s1}


filename = "constellations-list.txt"
f = open (filename)
lines = f.readlines ()
f.close ()

abbr_list = [s.strip().split("\t") for s in lines]
abbr_dict = {x[2]:x[0] for x in abbr_list}

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

for abbrev in args.files:
  starnums1 = unique (s2[abbrev])
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

  ax.annotate(abbr_dict [abbrev],             
    xy=(0.5, 0.5),  xycoords='figure fraction',
    xytext=(0.5, 0.5), textcoords='figure fraction',
    ha="center",va="center",weight='bold',
    fontsize=40, color='lightcoral', alpha=0.3, zorder=2
    )
  plt.scatter(lon, lat, transform=cr.PlateCarree(), zorder=3)

  plt.savefig (args.folder + "/" + abbrev + ".png")
  
  #plt.show() 


