import argparse
from src.ip_validations import *
from src.commands import exists_interface

def create_parse():
    epilog_text = """
Examples:

    #Enable dhcp config
    python netply enp0s8 dhcp

    #Enable dhcp config (defaults to dhcp if no configuration type is specified)
    python netply enp0s8

    #Enable static configuration
    python netply enp0s8 static -a 192.168.1.1/24

    #Configure gateway (defaults to "default" if no destination specified)
    python netply enp0s8 static -a 192.168.1.10/24 -t -v 192.168.1.1

    #Configure DNS
    python netply enp0s8 static -d 8.8.8.8 [1.1.1.1 [...]]

    """
    parse = argparse.ArgumentParser(
        prog="netply",
        description="Automate network configuration via Netplan on Ubuntu and derivative distributions",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter

    )

    #Positional arguments
    parse.add_argument("interface",type=exists_interface,help="network interface to configure")
    parse.add_argument("type",metavar="type",choices=["dhcp","static"],type=str,default="dhcp",nargs="?",help="The netplan configuration type (choices: dhcp, static)")

    #Core configurations
    parse.add_argument("-a","--address",metavar="IPv4/CIDR",type=validate_cidr,help="IPv4 address in CIDR notation. Example: 192.168.1.0/24" )
    parse.add_argument("-f","--force",action="store_true",help="Apply Netplan configuration without asking for confirmation")

    #DNS configuration
    parse.add_argument("-d","--dns-addresses",metavar="Ipv4",type=validate_dns,nargs="+",help="IPv4 DNS addresses")
    parse.add_argument("-s","--search",metavar="domain",type=str,help="specify DNS search domains")

    #Routing config
    parse.add_argument("-g","--gateway",metavar="IPv4",type=validate_ip,help="[DEPRECATED] specify the IPv4  gateway for Netplan configuration")
    parse.add_argument("-t","--to",metavar="IPv4/CIDR",type=validate_route_target,default="default",nargs='?',help="Specify the destination network. If the mask prefix is not specified, the program assumes that the IP is a individual host")
    parse.add_argument("-v","--via",metavar="IPv4 gateway",type=validate_ip,help="Specify the IPv4 gateway")

#   args = parse.parse_args()

    return parse

#parse = create_parse()
#arg = parse.parse_args()

