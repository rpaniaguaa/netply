import ipaddress
import argparse

def validate_cidr(cidr):
    """Validates if the string has the correct CIDR format"""

    if '/' not in cidr:
        raise argparse.ArgumentTypeError(f"'{cidr}' is missing the subnet mask prefix (e.g., /24). Example: 192.168.1.1/24")

    try:
        ip,_ = cidr.split("/")
        #la variable network se usará más adelante para validar si la ip es de red o broadcast
        network = ipaddress.IPv4Network(cidr, strict=False)
        #Separamos la ip del prefijo para realizar dicha validación
        ip_obj = ipaddress.IPv4Address(ip)
        
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{cidr}' is not valid Ipv4/CIDR anotation")

    if ip_obj == network.network_address:
        raise argparse.ArgumentTypeError(f"'{ip_obj}' is a network address. Please enter a valid host IP")
        
    if ip_obj == network.broadcast_address:
        raise argparse.ArgumentTypeError(f"'{ip_obj}' is a broadcast address. Please enter a valid host IP")

def validate_route_target(cidr):
    """Validates if the string has the correct CIDR format for network addresses"""

    if cidr == "default":
        return cidr

    if '/' not in cidr:
        cidr = f"{cidr}/32"

    try:
        return ipaddress.IPv4Network(cidr, strict=True)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{cidr}' is not a valid destination network or IPv4 address.")

def validate_ip(ip):
    """Validates if the string is a valid IP without the subnet mask prefix"""

    if '/' in ip:
        raise argparse.ArgumentTypeError(f"'{ip}' subnet mask prefix is not required")


    try:
        return ipaddress.IPv4Address(ip)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{ip}' is not a valid IPv4 address.")

