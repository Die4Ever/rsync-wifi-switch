#!/bin/bash

defaultwifi=wifiname
bandwidthwifi=otherwifiname

echo ""
lockfile -r 0 /run/lock/wifi.lock || exit 1
date
nmcli c | head -2
echo "...connecting to $bandwidthwifi..."
# disconnect from defaultwifi just in case you have 2 different wifi cards
nmcli c down "$defaultwifi"
nmcli c up "$bandwidthwifi"
exitcode=$?
if [ $exitcode != 0 ]; then rm -f /run/lock/wifi.lock ; exit $exitcode; fi

command=$1
shift
echo "...running $command..."
$command "$@"

date
echo "...connecting to $defaultwifi..."
nmcli c down "$bandwidthwifi"
nmcli c up "$defaultwifi"
nmcli c | head -2
rm -f /run/lock/wifi.lock

echo ""

