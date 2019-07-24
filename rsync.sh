#!/bin/bash

lockfile -r 0 /run/lock/rsync.lock || exit 1

# https://linux.die.net/man/1/rsync
# not using shorthand arguments because they get too confusing
# --force means force deletion of dirs even if not empty, probably only takes effect when --delete is used
# --modify-window=1 gives 1 seconds of margin of error for modification times, need this for NTFS, fine for other filesystems too
# --no-perms need this for NTFS, doesn't matter for other filesystems for our usecase
# --omit-dir-times might need this for NTFS, probably doesn't matter for other filesystems
date
rsync --update --delete --force --recursive --modify-window=2 --no-perms --human-readable --progress --stats --omit-dir-times $@
date
# show the disk space based on the last argument (the destination path)
echo -e "\ndone with rsync, outputting disk space"
df -h "${@: -1}"

rm -f /run/lock/rsync.lock
