#!/bin/bash
# Set correct work path (the one this script is in)
cd "${0%/*}"
# Execute the python script with the unbuffered python option for real time logging to file
python3 -u ./sensor.py > ./log.txt 2>&1 
