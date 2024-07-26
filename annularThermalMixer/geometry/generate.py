#!/usr/bin/python3

## Constant parts: outer wall, AMI interface patch, inner & outer outlets
##                 inner & outer inlets
## Parameter space for CAD design:
## - shaft radius
## - stator blade angle
## - blade radius, height, and tilting angle
## - nbr of blades per propeller 


import os, math
from stl import Mode
from madcad import *
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

cadDictPath = "./constant/cadDict"
cadDict = ParsedParameterFile(name=cadDictPath)

### General settings
radRes = ('rad', 0.01)
fixRes = ('fixed', 64)

### 1. Generate The shaft
shaft_base = Circle((O, Z), cadDict["shaft"]["radius"], resolution=radRes)
print(f"Generating shaft; radius = {cadDict['shaft']['radius']}; height = {cadDict['shaft']['height']}")
partial_trans = vec3(0,0, cadDict["shaft"]["height"])/fixRes[1]
shaft = repeat(
        extrusion(line=web(shaft_base), trans=transform(partial_trans)),
        fixRes[1],
        partial_trans)
shaft.finish()
write(mesh=shaft, name='shaft', type="stl", mode=Mode.ASCII)
os.rename('shaft', './constant/triSurface/shaft.stl')
shaft_hole = extrusion(partial_trans*fixRes[1], flatsurface(shaft_base).flip(), alignment=0.5)

### 2. Generate stator blades
def gen_stator_blades():
    n_blades = cadDict["stator"]["blades"]["n"]
    angle_on_oz = 2*math.pi/float(n_blades)
    s_blades = []
    for i in range(n_blades):
        A = vec3(cadDict["stator"]["blades"]["radius"]/2.0, 0, 0)
        s_blade_base = Segment(-A, A)
        s_blade = extrusion(
            line=web(s_blade_base),
            trans=transform(vec3(0,0,cadDict["stator"]["blades"]["height"]))
        ).transform(
            vec3(cadDict["stator"]["blades"]["distanceFromCenter"], 0, 0)
        ).transform(
            rotatearound(angle_on_oz*i, (O,Z))
        )
        s_blades.append(s_blade)
    blades = s_blades[0]
    for obj in s_blades[1:]:
        blades = union(blades, obj)
    return blades
print(f"Generating {cadDict['stator']['blades']['n']} stator blades")
s_blades = gen_stator_blades()
write(mesh=s_blades, name='statorBlades', type="stl", mode=Mode.ASCII)
os.rename('statorBlades', './constant/triSurface/statorBlades.stl')


### 3. Generate rotor blades
def gen_rotor_blades():
    n_blades = cadDict["rotor"]["blades"]["n"]
    angle_on_oz = 2*math.pi/float(n_blades)
    angle_on_ox = math.radians(cadDict["rotor"]["blades"]["tiltAngle"])
    z = cadDict["rotor"]["blades"]["height"]
    x = cadDict["shaft"]["radius"]+cadDict["rotor"]["blades"]["radius"]
    max_angle = math.degrees(math.atan(cadDict["shaft"]["radius"]/z))
    if cadDict["rotor"]["blades"]["tiltAngle"] < 0 or cadDict["rotor"]["blades"]["tiltAngle"] > max_angle:
        raise Exception(f"Rotation around X for rotor blades exceeds the feasible max angle: {max_angle:.2f}")
    r_blades = []
    for i in range(n_blades):
        print(f"rotating by {math.degrees(angle_on_oz*i)}")
        r_blade = flatsurface(
            wire([O, vec3(x,0,0), vec3(x,0,z), vec3(0,0,z)])
        ).transform(
            rotatearound(angle_on_ox, (O,X))
        ).transform(
            rotatearound(angle_on_oz*i, (O,Z))
        )
        r_blades.append(pierce(r_blade, shaft_hole))
    blades = r_blades[0]
    for obj in r_blades[1:]:
        blades = union(blades, obj)
    return blades
print(f"Generating {cadDict['rotor']['blades']['n']} rotor blades")
r_blades = gen_rotor_blades()
write(mesh=r_blades, name='rotorBlades', type="stl", mode=Mode.ASCII)
os.rename('rotorBlades', './constant/triSurface/rotorBlades.stl')
