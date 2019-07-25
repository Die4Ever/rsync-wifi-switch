#!/bin/bash

lockfile -r 3 /run/lock/wifi.lock || exit 1

read -p "Press [Enter] key to release wifi lock"

rm -f /run/lock/wifi.lock
