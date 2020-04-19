#!/bin/bash

lockfile -r 3 /run/lock/wifi.lock || exit 1

date
read -t 86400 -p "Press [Enter] key to release wifi lock (will timeout in 24 hours)"

rm -f /run/lock/wifi.lock
