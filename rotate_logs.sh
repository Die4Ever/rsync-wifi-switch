#!/bin/bash

cd "$(dirname "$0")"

rm rsync_log.txt.old
mv rsync_log.txt rsync_log.txt.old
touch rsync_log.txt
