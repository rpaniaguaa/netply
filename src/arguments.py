import argparse
import ipaddress

def is_valid_cidr(cidr):
    """Validates if the string has the correct CIDR format"""

    if '/' not in cidr:
        raise argparse.ArgumentTypeError(f"'{cidr}' is missing the subnet mask prefix (e.g., /24). Example: 192.168.1.1/24")

    try:
        return ipaddress.IPv4Network(cidr,strict=False)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{cidr}' is not a valid IPv4 address.")

def is_valid_ip(value):
    """Validates if the string is a valid IP without the subnet mask prefix"""

    if '/' in value:
        raise argparse.ArgumentTypeError(f"'{value}' subnet mask prefix is not required")


    try:
        return ipaddress.IPv4Address(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a valid IPv4 address.")


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
    parse.add_argument("-a","--address",metavar="IPv4/CIDR",type=is_valid_cidr,help="IPv4 address in CIDR notation. Example: 192.168.1.0/24" )
    parse.add_argument("-f","--force",action="store_true",help="Apply Netplan configuration without asking for confirmation")

    #DNS configuration
    parse.add_argument("-d","--dns-addresses",metavar="Ipv4",type=is_valid_ip,nargs="+",help="IPv4 DNS addresses (use it with -n)")
    parse.add_argument("-s","--search",metavar="domain",type=str,help="specify DNS search domains (use it with -n)")

    #Routing config
    parse.add_argument("-g","--gateway",metavar="IPv4",type=is_valid_ip,help="[DEPRECATED] specify the IPv4  gateway for Netplan configuration")
    parse.add_argument("-t","--to",metavar="IPv4 destination",type=is_valid_ip,default="default",nargs='?',help="Specify the destination host (use it with -r)")
    parse.add_argument("-v","--via",metavar="IPv4 gateway",type=is_valid_ip,help="Specify the IPv4 gateway (use it with -r)")


    args = parse.parse_args()
    

    return parse



parse = create_parse()


