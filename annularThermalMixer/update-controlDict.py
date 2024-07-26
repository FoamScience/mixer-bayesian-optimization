#!/usr/bin/python3

## Small script to update info in controlDict FOs from other case files

import math
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

control = ParsedParameterFile(name="./system/controlDict")
cad = ParsedParameterFile(name="./constant/cadDict")
settings = ParsedParameterFile(name="./constant/caseSettings")

control["functions"]["powerConsumption"]["radius"] = cad["shaft"]["radius"] + cad["rotor"]["blades"]["radius"]
control["functions"]["powerConsumption"]["n"] = settings["meshMotionProperties"]["omega"] / (2*math.pi)
control.writeFile()
