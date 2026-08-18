import os
import argparse

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
 
