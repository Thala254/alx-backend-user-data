#!/bin/bash
python3 -m $1 > /dev/null 2>&1 &
echo $! > $1.pid

sleep 3;