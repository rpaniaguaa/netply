import argparse

def parse_args():
    parse = argparse.ArgumentParser(description="A netplan configuration script")
    parse.add_argument("interface",type=str,help="network interface to configure")
    parse.add_argument("type",metavar="type",choices=["dhcp","static"],type=str,default="dhcp",nargs="?",help="The netplan configuration type (choices: dhcp, static)")
    return parse


parse = parse_args()
args = parse.parse_args()
print(args)