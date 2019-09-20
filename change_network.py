#!/usr/bin/python3 -u
# -*- coding: UTF-8 -*-# enable debugging
import subprocess
import re
import argparse
import sys
import os
import time

#flush after every print
import functools
print = functools.partial(print, flush=True)

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--network', type=str, help='Network to use for running the command')
parser.add_argument('--default-network', type=str, help='Network to switch to after running the command')
parser.add_argument('--check-seconds', type=int, help='How long in seconds to check if a network is in use', default=120)
(args, command) = parser.parse_known_args()
wifi_locked = False

def main():
    global args
    ret = 1
    if set_network(args.network):
        ret = run_command()
    if args.default_network:
        set_network(args.default_network)
    wifi_unlock()
    print("exiting with code "+str(ret))
    exit(ret)


def calla(cmds):
    print("running", cmds)
    ret = subprocess.Popen(cmds).wait()
    print("exit code == "+str(ret))
    return ret

def call(cmd):
    print("running", cmd)
    ret = subprocess.Popen(cmd, shell=True).wait()
    print("exit code == "+str(ret))
    return ret

def run_command():
    global command
    print()
    if len(command) == 0:
        print("no command to run")
        return 0
    ret = calla(command)
    print()
    return ret

def check_output(cmds):
    print("running", cmds)
    ret = subprocess.check_output(cmds).decode("utf-8")
    #print("command got\n" + ret)
    return ret

def get_current_network():
    out = check_output(["nmcli", "-t", "--color=no", "c"])
    line = out.splitlines()[0]
    s = line.split(':')
    net = s[0]
    inf = s[3]
    print("current network == "+net+", interface == "+inf)
    return (net, inf)

def connect(network):
    print("connecting to "+network)
    ret = calla(["nmcli", "c", "up", network])
    time.sleep(2)
    return ret

def disconnect(network):
    print("disconnecting from "+network)
    return calla(["nmcli", "c", "down", network])

def set_network(network):
    print("\n\nset_network("+network+")")
    (current, inf) = get_current_network()
    if current == network:
        print("we're already on "+current+", continuing")
        return True
    if network_in_use(inf):
        print(current+" is currently in use, bailing")
        return False
    if wifi_lock() == False:
        print("failed to aquire wifi lock, bailing")
        return False
    disconnect(current)
    ret = connect(network)
    return ret == 0

def test_network():
    #make sure the connection works
    print("this is where I would test the network to make sure it can reach the internet")
    #calla(["echo", "test_network"])

def network_in_use(inf):
    # MPC seems to buffer heavily over SMB, so might need to use 120 seconds
    global args
    ms = args.check_seconds * 1000
    out = check_output(["bwm-ng",  "-o",  "csv",  "-t", str(ms), "-c",  "1"])
    lines = out.splitlines()
    for line in lines:
        split = line.split(';')
        if split[1] == inf:
            Bps = float(split[4])
            MBps = Bps / (1024 * 1024)
            print(inf+" is doing "+str(MBps)+" MBps")
            if MBps > 0.1:
                return True
            else:
                return False
    return False

def wifi_lock():
    global wifi_locked
    # do I even need wifi locking anymore?
    # I already have the cron.lock and rsync.lock, and I check if the network is in use before switching...
    if wifi_locked:
        return True
    ret = calla(["lockfile", "-r", "0", "/run/lock/wifi.lock"])
    if ret == 0:
        wifi_locked=True
        return True
    return False

def wifi_unlock():
    global wifi_locked
    ret = 0
    if wifi_locked:
        ret = calla(["rm", "-f", "/run/lock/wifi.lock"])
    if ret == 0:
        wifi_locked = False
        return True
    return False

if __name__=="__main__":
    main()

