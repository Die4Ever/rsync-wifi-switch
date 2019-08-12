#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-# enable debugging
import subprocess
import re
import argparse

parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--network', type=str)
#parser.add_argument('--command', type=str, default='')
parser.add_argument('command', nargs='*', help='Command to run')
args = parser.parse_args()
wifi_locked = False

def calla(cmds):
    print("running", cmds)
    ret = 0 #subprocess.Popen(cmds).wait()
    print("exit code == "+str(ret))
    return ret

def call(cmd):
    print("running", cmd)
    ret = 0 #subprocess.Popen(cmd, shell=True).wait()
    print("exit code == "+str(ret))
    return ret

def run_command():
    global args
    if len(args.command) == 0:
        return 0
    return calla(args.command)

def check_output(cmds):
    print("running", cmds)
    ret = subprocess.check_output(cmds).decode("utf-8")
    print("command got\n" + ret)
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
    return calla(["nmcli", "c", "up", network])

def disconnect(network):
    print("disconnecting from "+network)
    return calla(["nmcli", "c", "down", network])

def set_network(network):
    (current, inf) = get_current_network()
    if current == network:
        return True
    if network_in_use(inf):
        return False
    if wifi_lock() == False:
        return False
    disconnect(current)
    ret = connect(network)
    ret = run_command()
    wifi_unlock()
    return ret

def test_network():
    #make sure the connection works
    calla(["echo", "test_network"])

def network_in_use(inf):
    #out = check_output(["bwm-ng",  "-o",  "csv",  "-t", "120000", "-c",  "1"])
    out = check_output(["bwm-ng",  "-o",  "csv",  "-t", "1000", "-c",  "1"])
    return False

def wifi_lock():
    global wifi_locked
    ret = calla(["lockfile", "-r", "0", "/run/lock/wifi.lock"])
    if ret == 0:
        wifi_locked=True
        return True
    return False

def wifi_unlock():
    global wifi_locked
    if wifi_locked:
        ret = calla(["rm", "-f", "/run/lock/wifi.lock"])

set_network(args.network)
