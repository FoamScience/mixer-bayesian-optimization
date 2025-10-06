#!/usr/bin/env bash

set -e
if [ ! -f ./postProcessing/powerConsumption/0/propellerPerformance.dat ]; then
    echo nan
    exit 0
fi

has_data=$(awk -v found=0 '/^[0-9]/{found=1} END{if (found) print "yes"}' postProcessing/powerConsumption/0/propellerPerformance.dat)
if [ -z $has_data ]; then
    echo nan
    exit 0
fi

R=$(awk '/# Radius/ {print $4+0}' ./postProcessing/powerConsumption/0/propellerPerformance.dat)
n=$(tail -1 ./postProcessing/powerConsumption/0/propellerPerformance.dat | awk '{print $2+0}')
KQ=$(tail -1 ./postProcessing/powerConsumption/0/propellerPerformance.dat | awk '{print $6/10}')
awk -v KQ=$KQ -v n=$n -v R=$R 'BEGIN {print 2*atan2(0,-1)*KQ*n^3*(2*R)^5}'
