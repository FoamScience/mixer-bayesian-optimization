#!/usr/bin/env bash
casename=$(basename $PWD)
didUpload=false
if test -e url; then
    cat url
else
    pvpython --force-offscreen-rendering ./render-results.py . $casename > /dev/null 2>&1
    convert  $casename.png -transparent white -trim -resize 90% $casename.png
    curl -s --location --request POST "https://api.imgbb.com/1/upload?expiration=600&key=${IMGBB_API_KEY}"\
    --form "image=@./$casename.png" | jq .data.url | tee url
fi
