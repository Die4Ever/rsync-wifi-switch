#!/bin/bash

cd "$(dirname "$0")"

{

lockfile -r 0 /run/lock/cron.lock || exit 1

defaultwifi=wifiname
bandwidthwifi=otherwifiname

command=$1
shift
#check if there are any changes to reduce how often we switch networks
$command --dry-run $@ | grep 'Number of regular files transferred: 0foobar'
exitcode=$?
if [ $exitcode == 1 ]; then python3 change_network.py --network="$bandwidthwifi" --default-network="$defaultwifi" $command "$@" ; fi

rm -f /run/lock/cron.lock
} >>rsync_log.txt 2>&1

