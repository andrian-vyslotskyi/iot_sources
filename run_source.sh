#!/usr/bin/env bash

#------------
# -lrst
#------------

OPTIONS=lrst
LONGOPTIONS=light,rain,soil,temperature

# -temporarily store output to be able to check for errors
# -activate advanced mode getopt quoting e.g. via “--options”
# -pass arguments only via   -- "$@"   to separate them correctly
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
    # e.g. $? == 1
    #  then getopt has complained about wrong arguments to stdout
    exit 1
fi
# use eval with "$PARSED" to properly handle the quoting
eval set -- "${PARSED}"

#-----------------------------------------------------------------
#mode initialization
light_run=false
rain_run=false
soil_run=false
temperature_run=false
#-----------------------------------------------------------------
while true; do
    case "$1" in
        -l|--light)
            light_run=true
            shift
            ;;
        -r|--rain)
            rain_run=true
            shift
            ;;
        -t|--temperature)
            temperature_run=true
            shift
            ;;
        -s|--soil)
            soil_run=true
            shift
            ;;
        -o|--output)
            outFile="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 2
            ;;
    esac
done

if [[ ${soil_run} = true ]]; then
    python2 sources/soil.py &
fi


if [[ ${temperature_run} = true ]]; then
    python2 sources/th.py &
fi

if [[ ${light_run} = true ]]; then
    python2 sources/light.py &
fi


if [[ ${rain_run} = true ]]; then
    python2 sources/rain.py &
fi