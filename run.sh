#!/bin/bash

Xvfb :99 &
export DISPLAY=:99
export WINEDEBUG=-all

python3 -u miner.py
