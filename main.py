import src.arguments
import argparse
import src.commands
from src.netpan_config import NetplanConf
def main():
    NETPLAN_FILE = '/etc/netplan/test.yaml'
    '''
    if not src.commands.is_root():
        print("error: cannot access file: permission denied")
        exit(1)
    '''
    if not src.commands.exists_netplan_config(NETPLAN_FILE):
        print(f"error: '{NETPLAN_FILE}' does not exists")
        exit(2)
        
    parse = src.arguments.create_parse()
    args = parse.parse_args()
    netplan = NetplanConf(args,NETPLAN_FILE)
    static_args = any([
        args.address is not None,
        args.dns_addresses is not None,
        args.search is not None, 
        args.gateway is not None,
        args.to != 'default',
        args.via is not None       
    ])
    
    if args.type == 'dhcp' and static_args:
        print("error: 'dhcp' cannot be used with any static parameter")
        exit(3)

    if args.type == 'static' and not static_args:
        print("error: 'static' requires at least --address parameter")
        exit(3)

    if args.type == 'dhcp':
        netplan.dhcp_conf()

if __name__ == '__main__':
    main()