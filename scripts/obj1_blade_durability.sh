#!/usr/bin/env bash

# Computes blade durability for latest time step

set -e
if [ ! -d processor0 ]; then
    echo nan
    exit 0
fi
times_step=$(foamListTimes  -case processor0 | tail -1) || echo nan
if [ -z "$times_step" ]; then
    echo nan
    exit 0
fi

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
dur=$(pvpython "$SCRIPT_DIR"/blade-durability.py . "$times_step")
nBlades=$(foamDictionary -entry rotor.blades.n -value ./constant/cadDict)
awk "BEGIN{print($dur/$nBlades)}" || echo nan
