#!/bin/bash
# Set correct work path (the one this script is in)
cd "${0%/*}"
python3 AutomaticOctoprintLED.py &> /dev/null
