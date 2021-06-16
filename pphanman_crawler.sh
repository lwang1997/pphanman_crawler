#!/bin/bash
pid=""
heart_beat=""

function start {
    ./pphanman_crawler.py &
    pid=$!
}

function stop {
    kill $pid
}

function killall {
    kill $pid
}

trap "killall" SIGINT


while [[ True ]]; do
    start
    sleep 300
    new_heart_beat=`cat /tmp/pphanman_crawler.lock`

    if [[ "$heart_beat" == "$new_heart_beat" ]]; then
        echo "crawler got stuck, restart"
        stop
        start
    fi
    heart_beat=$new_heart_beat
done
