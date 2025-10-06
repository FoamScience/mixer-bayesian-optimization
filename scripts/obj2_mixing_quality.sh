#!/usr/bin/env bash

set -e
if [ ! -f ./postProcessing/mixingQuality/0/volFieldValue.dat ]; then
    echo nan
    exit 0
fi

tail -1 ./postProcessing/mixingQuality/0/volFieldValue.dat | awk '{print($2+0)}' || echo nan
