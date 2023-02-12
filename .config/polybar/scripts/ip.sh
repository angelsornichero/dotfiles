#!/bin/sh

echo "%{F#AD69AF}󰴽 %{F#ffffff}$(ip address | grep 'dynamic' | cut -d ' ' -f 8)%{u-}"
