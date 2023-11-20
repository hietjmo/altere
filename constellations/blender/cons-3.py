
import bpy
import os
import sys
from math import cos,tau,sin,sqrt
import numpy as np

dir1 = os.path.dirname (bpy.data.filepath)
if not dir1 in sys.path:
    sys.path.append (dir1)

from stars import stars,abbrs,borders,ccolors

r = 10.0
cons1 = {}

def from_hex (h):
  return tuple (round (int(h.lstrip('#')[i:i+2], 16)/255,2) for i in (0,2,4))

p1 = [ 
  "#e41a1c",
  "#377eb8",
  "#4daf4a",
  "#984ea3",
  "#ff7f00",
  "#ffff33",
  "#a65628",
  "#f781bf",
  "#999999",]
p2 = ['red', 'blue', 'green', 'violet', 'orange', 'yellow', 'brown', 'pink', 'grey']
palette1 = [from_hex (h) for h in p1]
palette3 = dict (zip(p2,palette1))

def rad (deg):
  return tau * deg / 360

num = 0
for cons in stars:
  cons1 [cons] = []
  for ra,dec,mag in stars[cons]:
    theta = rad (ra)
    phi = rad (dec)
    x = r * cos (phi) * cos (theta)
    y = r * cos (phi) * sin (theta)
    z = r * sin (phi)
    cons1 [cons].append ((x,y,z,mag))
    num = num + 1

message = f"Create {num} objects. This may take a while..."
print (message)

# Create a new materials
materials = {}
for name in palette3:
  rgb = palette3 [name]
  material = bpy.data.materials.new (name=name)
  material.use_nodes = True
  nodes = material.node_tree.nodes
  emission_node = nodes.new (type='ShaderNodeEmission')
  material.node_tree.links.new (
    emission_node.outputs["Emission"], 
    nodes["Material Output"].inputs["Surface"])
  emission_node.inputs["Strength"].default_value = 2.0
  materials [name] = material.copy()
  materials [name].node_tree.nodes [
    "Emission"].inputs[0].default_value = (rgb[0],rgb[1],rgb[2],1.0)

for cons in cons1:
  for x,y,z,mag in cons1[cons]:
    collection_name = "North" if z >= 0.0 else "South"
    bpy.ops.mesh.primitive_ico_sphere_add (radius=0.1, location=(x, y, z))
    star = bpy.context.active_object
    star.data.materials.append (materials[ccolors[cons]])
    star.name = cons
    collection = bpy.data.collections.get (collection_name)
    # Check if the collection exists
    if collection is not None:
      # Link the object to the collection
      collection.objects.link (star)
    else:
      # If the collection doesn't exist, create it and link the object
      collection = bpy.data.collections.new (collection_name)
      bpy.context.scene.collection.children.link (collection)
      collection.objects.link (star)
    bpy.context.scene.collection.children['Collection'].objects.unlink (star)

# Set the desired 3D Viewport shading type
desired_shading_type = 'RENDERED'

# Find the 3D Viewport space
for area in bpy.context.screen.areas:
  if area.type == 'VIEW_3D':
    for space in area.spaces:
      if space.type == 'VIEW_3D':
        # Set the shading type
        space.shading.type = desired_shading_type
        break
    break

