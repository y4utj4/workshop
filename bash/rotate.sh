#!/bin/zsh

echo -n "Enter Rotate Direction: \n"
read direction
xrandr --output DP-2-2 --rotate $direction