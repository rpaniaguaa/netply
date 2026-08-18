import argparse
import os
import subprocess

### Validate interfaces ###

def get_interfaces():
    path = "/sys/class/net/"
    return [iface for iface in os.listdir(path) if iface != 'lo']


def exists_interface(iface):

    if iface == 'lo':
        raise argparse.ArgumentTypeError(f"'{iface}' is not a valid interface")

    elif iface not in get_interfaces():
        raise argparse.ArgumentTypeError(f"'{iface}' does not exist")
    
    else:
        return iface


### Validate admin user ###

def is_root():
    return os.geteuid() == 0


### Validate if netplan config file exists ###

def exists_netplan_config(NETPLAN_FILE):
    return os.path.isfile(NETPLAN_FILE)
