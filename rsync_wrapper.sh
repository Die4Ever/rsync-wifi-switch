#!/bin/bash

cd "$(dirname "$0")"

{

./rsync.sh $@

} >>rsync_log.txt 2>&1

