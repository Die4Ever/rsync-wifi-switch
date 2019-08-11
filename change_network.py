#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-# enable debugging
import subprocess
import re

def calla(cmds):
    return subprocess.Popen(cmds).wait()

def call(cmd):
    return subprocess.Popen(cmd, shell=True).wait()

def run_command():
    #do the thing
    command = "echo 'hi'"
    return call(command)

def check_output(cmds):
    return subprocess.check_output(cmds)

def get_current_network():
    out = check_output(["nmcli", "c"])

def connect(network):
    calla(["nmcli", "c", "up", network])

def disconnect(network):
    calla(["nmcli", "c", "down", network])

def set_network(network):
    current = get_current_network()
    if current == network:
        return True
    if network_in_use():
        return False
    if wifi_lock() == False:
        return False
    disconnect(current)
    connect(network)
    ret = run_command()
    wifi_unlock()
    return ret

def test_network():
    #make sure the connection works

def network_in_use():
    out = check_output(["bwm-ng",  "-o",  "csv",  "-t", "120000", "-c",  "1"])
    return False

def wifi_lock():
    ret = calla(["lockfile", "-r", "0", "/run/lock/wifi.lock"])

def wifi_unlock():
    ret = calla(["rm", "-f", "/run/lock/wifi.lock"])

