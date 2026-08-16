import argparse
from ip_validations import *

def create_parse():
    epilog_text = """
Examples:

    #Enable dhcp config
    python3 netply enp0s8 dhcp

    #Enable dhcp config (defaults to dhcp if no configuration type is specified)
    python3 netply enp0s8 

    """
    parse = argparse.ArgumentParser(
        prog="netply",
        description="Automate network configuration via Netplan on Ubuntu and derivative distributions",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter

    )

    #Positional arguments
    parse.add_argument("interface",type=str,help="network interface to configure")
    parse.add_argument("type",metavar="type",choices=["dhcp","static"],type=str,default="dhcp",nargs="?",help="The netplan configuration type (choices: dhcp, static)")

    #Core configurations
    parse.add_argument("-a","--address",metavar="IPv4/CIDR",type=validate_cidr,help="IPv4 address in CIDR notation. Example: 192.168.1.0/24" )
    parse.add_argument("-f","--force",action="store_true",help="Apply Netplan configuration without asking for confirmation")

    #DNS configuration
    parse.add_argument("-d","--dns-addresses",metavar="Ipv4",type=validate_ip,nargs="+",help="IPv4 DNS addresses")
    parse.add_argument("-s","--search",metavar="domain",type=str,help="specify DNS search domains")

    #Routing config
    parse.add_argument("-g","--gateway",metavar="IPv4",type=validate_ip,help="[DEPRECATED] specify the IPv4  gateway for Netplan configuration")
    parse.add_argument("-t","--to",metavar="IPv4/CIDR",type=validate_route_target,default="default",nargs='?',help="Specify the destination network. If the mask prefix is not specified, the program assumes that the IP is a individual host")
    parse.add_argument("-v","--via",metavar="IPv4 gateway",type=validate_ip,help="Specify the IPv4 gateway")

    return parse


