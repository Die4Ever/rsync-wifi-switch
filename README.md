# rsync-wifi-switch

you'll need to install procmail in order to get lockfile

the scripts all adjust their current working directory and automatically redirect their output to rsync_log.txt which gets rotated to rsync_log.txt at midnight if you use the example crontab

check the example crontab for how to use this, you can also skip the check_rsync and change_network stuff if you're not worried about that, then your crontab entry would look like (rsync_wrapper.sh adjusts the working directory and redirects the output to the log, which is nice when running as a cron)

\# make sure to test with --dry-run first
*/10 * * * * rsync-wifi-switch/rsync_wrapper.sh --dry-run --include-from=rsync_list.txt user@servername:"./" "~/downloads/"

you'll also need to make rsync_list.txt, look at example_rsync_list.txt to see how it works or just look up how --include-from filters work in rsync

if you want to get rid of the file that this downloaded without adjusting filters, you can easily just do
echo "" > dumbfile.zip
this will empty the file and update the modified time, so rsync won't overwrite a newer file
you can also use the touch command to set the modified date to the future
