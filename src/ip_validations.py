import ipaddress
import argparse

def validate_cidr(cidr):
    """Validates if the string has the correct CIDR format"""

    if '/' not in cidr:
        raise argparse.ArgumentTypeError(f"'{cidr}' is missing the subnet mask prefix (e.g., /24). Example: 192.168.1.1/24")

    try:
        ip,_ = cidr.split("/")
        #network variable is used to validate if the ip is a network or a broadcast address
        network = ipaddress.IPv4Network(cidr, strict=False)
        #we separate the IP from the mask to get the host 
        ip_obj = ipaddress.IPv4Address(ip)

        if ip_obj == network.network_address:
                raise argparse.ArgumentTypeError(f"'{ip_obj}' is a network address. Please enter a valid host IP")
                
        elif ip_obj == network.broadcast_address:
                raise argparse.ArgumentTypeError(f"'{ip_obj}' is a broadcast address. Please enter a valid host IP")

        elif  ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved:
            raise argparse.ArgumentTypeError(f"'{ip}' is not a valid host. Please enter a valid host IP")

        else:
            return cidr  
        
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{cidr}' is not valid Ipv4/CIDR anotation")

    
def validate_route_target(cidr):
    """Validates if the string has the correct CIDR format for network addresses"""

    if cidr == "default":
        return cidr

    try:
        if '/' not in cidr:
            cidr = f"{cidr}/32"

        ip,_ = cidr.split('/')

        ip_str = ipaddress.IPv4Address(ip)
        if  ip_str.is_loopback or ip_str.is_link_local or ip_str.is_multicast or ip_str.is_reserved:
            raise argparse.ArgumentTypeError(f"'{cidr}' is not a valid destination network or IPv4 address.")
        
        return ipaddress.IPv4Network(cidr, strict=True)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{cidr}' is not a valid IPv4 address.")

def validate_ip(ip):
    """Validates if the string is a valid IP without the subnet mask prefix"""

    if '/' in ip:
        raise argparse.ArgumentTypeError(f"'{ip}' subnet mask prefix is not required")


    try:
        ip_str = ipaddress.ip_address(ip)

        if  ip_str.is_loopback or ip_str.is_link_local or ip_str.is_multicast or ip_str.is_reserved or str(ip_str) == '0.0.0.0':
            raise argparse.ArgumentTypeError(f"'{ip}' is not a valid host")
        else:
            return ip
        
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{ip}' is not a valid IPv4 address.")


def validate_dns(ip):
    """Validates if the string is a valid IP without the subnet mask prefix for DNS"""

    if '/' in ip:
        raise argparse.ArgumentTypeError(f"'{ip}' subnet mask prefix is not required")


    try:
        ip_str = ipaddress.ip_address(ip)
        #loopback addresses in DNS are allowed
        if  ip_str.is_link_local or ip_str.is_multicast or ip_str.is_reserved or str(ip_str) == '0.0.0.0':
            raise argparse.ArgumentTypeError(f"'{ip}' is not a valid host")
        else:
            return ip
        
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{ip}' is not a valid IPv4 address.")

