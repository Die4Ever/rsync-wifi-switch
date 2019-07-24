#!/bin/bash

cd "$(dirname "$0")"

{

command=$1
shift
#check if there are any changes to reduce how often we switch networks
$command --dry-run $@ | grep 'Number of regular files transferred: 0'
exitcode=$?
if [ $exitcode == 1 ]; then ./change_network.sh $command "$@" ; fi

} >>rsync_log.txt 2>&1

