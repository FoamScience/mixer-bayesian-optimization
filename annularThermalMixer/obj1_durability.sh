#!/usr/bin/bash

source /usr/lib/openfoam/openfoam2312/etc/bashrc
dur=$(pvpython ./blade-durability.py . 1.0)
nBlades=$(foamDictionary -entry rotor.blades.n -value ./constant/cadDict)
awk "BEGIN{print($dur/$nBlades)}"
