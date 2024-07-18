#!/usr/bin/bash

omega=$(awk '/omega.*;/ {print($2*atan2(0, -1)/180)}' ./constant/caseSettings)
torque=$(tail -1 ./postProcessing/powerConsumption/0/propellerPerformance.dat | cut -f6 | awk '{print $0+0}')
echo "$omega*$torque" | bc
