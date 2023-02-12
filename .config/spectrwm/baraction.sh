#!/bin/bash

# baraction.sh for spectrwm status bar
# https://github.com/conformal/spectrwm

# Antonio Sarosi
# https://youtube.com/c/antoniosarosi
# https://github.com/antoniosarosi/dotfiles

icon() {
    echo -n "+@fg=1;$1+@fg=0;"
}

percentage() {
    current=`echo $1 | sed 's/%//'`
    if [ $current -le 25 ]; then 
        echo -n "$(icon $2)"
    elif [ $current -le 50 ]; then
        echo -n "$(icon $3)"
    elif [ $current -le 75 ]; then
        echo -n "$(icon $4)"
    else
        echo -n "$(icon $5)"
    fi
}

sleep_sec=2
i=0
while :; do
    # CPU
    cpu=`lscpu | grep 'CPU(s) scaling MHz' | tr -d '[[:space:]]' | cut -d ':' -f 2`
    echo -n "$(icon 󰅒) $cpu "
    # Memory
    memory=`free -h | grep "Mem" | sed 's/       / /g' | cut -d ' ' -f 8`
    echo -n "$(icon 󰍛) $memory "
    # Updates
    if (( $i % 60 == 0 )); then
        updates=`checkupdates | wc -l`
    fi
    echo -n "$(icon  ) $updates "

    # Brightness
    (( br = $(brightnessctl get) * 100 / 6818 ))
    echo -n "$(percentage $br        ) $br% "

    # Battery
    if (( $i % 60 == 0 )); then
        bat=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 |
            grep percentage |
            sed 's/ *percentage: *//g'`

        state=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 |
            grep state |
            sed 's/ *state: *//'`
    fi
    if [ $state == "charging" -o $state == "fully-charged" ]; then
        echo -n "$(icon  ) "
    else
        echo -n "$(percentage $bat            )  "
    fi
    echo -n "$bat "

    # Date
    if (( $i % 60 == 0 )); then
        dte="$(date +"$(icon  ) %H:%M")"
        
    fi
    echo -e "$dte"

	sleep $sleep_sec
    (( i += $sleep_sec ))
done
