import argparse

def parse_args():
    epilog_text = """
Examples:

    #Enable dhcp config
    python3 netply enp0s8 dhcp

    #Enable dhcp config (defaults to dhcp if no configuration type is specified)
    python3 netply enp0s8 

    """
    parse = argparse.ArgumentParser(
        prog="netply",
        description="Automate network configuration via Netplan on Ubuntu and derivate distributions",
        epilog=epilog_text,
        formatter_class=argparse.RawDescriptionHelpFormatter

    )

    parse.add_argument("interface",type=str,help="network interface to configure")
    parse.add_argument("type",metavar="type",choices=["dhcp","static"],type=str,default="dhcp",nargs="?",help="The netplan configuration type (choices: dhcp, static)")
    parse.add_argument("-a","--address",metavar="IPv4/CIDR",type=str,help="IPv4 address in CIDR notation. Example: 192.168.1.0/24" )
    parse.add_argument("-f","--force",action="store_true",help="Apply Netplan configuration without asking for confirmation")

    #DNS configuration
    parse.add_argument("-d","--dns-addresses",metavar="Ipv4",type=str,nargs="+",help="IPv4 DNS addresses (use it with -n)")
    parse.add_argument("-n","--nameservers",action="store_true",help="enable the dns configuration")
    parse.add_argument("-s","--search",metavar="domain",type=str,help="specify DNS search domains (use it with -n)")

    #Routing config
    parse.add_argument("-g","--gateway",metavar="IPv4",type=str,help="[DEPRECATED] specify the IPv4  gateway for Netplan configuration")
    parse.add_argument("-r","--route",action="store_true",help="enable the routing config (use this option instead of -g)")
    parse.add_argument("-t","--to",metavar="IPv4 destination",type=str,default="default",nargs='?',help="Specify the destination host (use it with -r)")
    parse.add_argument("-v","--via",metavar="IPv4 gateway",type=str,help="Specify the IPv4 gateway (use it with -r)")

    return parse


parse = parse_args()
args = parse.parse_args()
print(args)