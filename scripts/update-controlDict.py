#!/usr/bin/python3

# /// script
# requires-python = ">=3.12"
# dependencies = [ "foamlib>=1.3.11" ]
# ///

## Small script to update info in controlDict FOs from other case files

from foamlib import FoamFile

control = FoamFile("./system/controlDict")
cad = FoamFile("./constant/cadDict")
settings = FoamFile("./constant/caseSettings")

control["functions"]["powerConsumption"]["radius"] = cad["shaft"]["radius"] + cad["rotor"]["blades"]["radius"]
control["functions"]["powerConsumption"]["n"] = settings["meshMotionProperties"]["omega"] / 360.0
