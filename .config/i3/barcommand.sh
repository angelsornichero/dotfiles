#!/bin/bash

icon() {
    echo -n "$1"
}

sleep_sec=2
i=0
while :; do 
    # Date
    if (( $i % 60 == 0 )); then
        dte="$(date +"$(icon  ) %H:%M")"
        
    fi
    echo -e "$dte"

	sleep $sleep_sec
    (( i += $sleep_sec ))
done
